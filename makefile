#
# makefile for crippy
#

# Windows only -> Powershell
SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command
OUT_NEW := | Out-File -Encoding default
OUT_APP := | Out-File -Encoding default -Append

# names (directories & files)
SCRIPT_NAME := crippy
ICON_FILE := python.ico
ICON_NAME := python-icon.svg
VENV_DIR := .venv
BUILD_DIR := build
BUILD_TARGET_DIR := dist
BUILD_INFO := build_info.txt
PRE_BUILD_CLEAN := @("$(BUILD_DIR)", "$(BUILD_TARGET_DIR)", "$(SCRIPT_NAME).spec", "$(SCRIPT_NAME)_info.txt")
COVERAGE_HTML := coverage_html
INNO_SETUP = setup.iss
INNO_VERSION = version.iss

# binaries / executables
UV := uv
VENV := .\$(VENV_DIR)\Scripts
VENV_ACTIVATE := $(VENV)\activate.ps1
VENV_PYTHON := $(VENV)\python.exe
PYTEST := $(VENV)\pytest.exe
PYINSTALLER := $(VENV)\pyinstaller.exe
PYSIDE6_UIC := $(VENV)\pyside6-uic.exe
PYSIDE6_RCC := $(VENV)\pyside6-rcc.exe
QT_DESIGNER := $(VENV_DIR)\Lib\site-packages\PySide6\designer.exe
MAKE_INNO := "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

all: build

.NOTPARALLEL:

init: $(VENV_ACTIVATE)

$(VENV_ACTIVATE):
	$(UV) venv
    ifeq (,$(wildcard requirements.txt))
		$(UV) pip compile pyproject.toml -o requirements.txt
    endif
    ifeq (,$(wildcard dev-requirements.txt))
		$(UV) pip compile pyproject.toml --extra dev -o dev-requirements.txt
    endif
	$(UV) pip sync dev-requirements.txt --require-hashes --allow-empty-requirements

requirements.txt: $(VENV_ACTIVATE) pyproject.toml
	$(UV) pip compile pyproject.toml -o requirements.txt

dev-requirements.txt: $(VENV_ACTIVATE) pyproject.toml
	$(UV) pip compile pyproject.toml --extra dev -o dev-requirements.txt 

.PHONY: upgrade_uv
upgrade_uv: $(VENV_ACTIVATE)
	$(UV) self update

.PHONY: upgrade_requirements
upgrade_requirements: $(VENV_ACTIVATE)
	$(UV) pip compile pyproject.toml --upgrade -o requirements.txt
	$(UV) pip compile pyproject.toml --upgrade --extra dev -o dev-requirements.txt

.PHONY: upgrade_all
upgrade_all: upgrade_uv upgrade_requirements sync

.PHONY: sync
sync: $(VENV_ACTIVATE) requirements.txt dev-requirements.txt
	$(UV) pip sync dev-requirements.txt --require-hashes --allow-empty-requirements

.PHONY: list
list: $(VENV_ACTIVATE)
	$(UV) pip list

.PHONY: qt_designer
qt_designer: $(VENV_ACTIVATE)
	$(QT_DESIGNER) $(SCRIPT_NAME).ui

$(SCRIPT_NAME)_ui.py: $(SCRIPT_NAME).ui
	$(PYSIDE6_UIC) -o $(SCRIPT_NAME)_ui.py $(SCRIPT_NAME).ui

$(SCRIPT_NAME)_rc.py: $(SCRIPT_NAME).qrc $(ICON_NAME)
	$(PYSIDE6_RCC) -o $(SCRIPT_NAME)_rc.py $(SCRIPT_NAME).qrc

.PHONY: test
test: $(VENV_ACTIVATE)
	$(VENV_PYTHON) test_$(SCRIPT_NAME)_app.py

.PHONY: run
run: $(VENV_ACTIVATE) $(SCRIPT_NAME)_ui.py $(SCRIPT_NAME)_rc.py
	$(VENV_PYTHON) $(SCRIPT_NAME).py

.PHONY: build
build: $(VENV_ACTIVATE) $(SCRIPT_NAME)_ui.py $(SCRIPT_NAME)_rc.py
	foreach ($$item in $(PRE_BUILD_CLEAN)) { if (Test-Path -LiteralPath $$item) { Remove-Item -LiteralPath $$item -Force -Recurse }}
	$(VENV_PYTHON) mk_file_version_info.py --out $(SCRIPT_NAME)_info.txt $(SCRIPT_NAME).py
	$(PYINSTALLER) --version-file $(SCRIPT_NAME)_info.txt --contents-directory lib --icon=$(ICON_FILE) --noconsole $(SCRIPT_NAME).py
	$(VENV_PYTHON) -c "import sys; import datetime; print(f'Python {sys.version}'); print(f'Build time: {datetime.datetime.now().astimezone()}\n')" $(OUT_NEW) $(BUILD_INFO)
	$(UV) pip list $(OUT_APP) $(BUILD_INFO)
	$(VENV_PYTHON) -c "import datetime as dt; dq=chr(34); ts=dt.datetime.now().strftime('%Y.%m.%d.%H%M%S'); print(f'#define MyAppVersion {dq}{ts}{dq}')" $(OUT_NEW) $(INNO_VERSION)
	& $(MAKE_INNO) $(INNO_SETUP)
