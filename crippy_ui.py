# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crippy.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

from myplaintextedit import MyPlainTextEdit
import crippy_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(639, 594)
        icon = QIcon()
        icon.addFile(u":/images/python-icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.file_exit = QAction(MainWindow)
        self.file_exit.setObjectName(u"file_exit")
        self.help_about = QAction(MainWindow)
        self.help_about.setObjectName(u"help_about")
        self.file_open = QAction(MainWindow)
        self.file_open.setObjectName(u"file_open")
        self.file_save = QAction(MainWindow)
        self.file_save.setObjectName(u"file_save")
        self.file_new = QAction(MainWindow)
        self.file_new.setObjectName(u"file_new")
        self.encrypt_input_to_output = QAction(MainWindow)
        self.encrypt_input_to_output.setObjectName(u"encrypt_input_to_output")
        self.encrypt_file_to_output = QAction(MainWindow)
        self.encrypt_file_to_output.setObjectName(u"encrypt_file_to_output")
        self.decrypt_input_to_output = QAction(MainWindow)
        self.decrypt_input_to_output.setObjectName(u"decrypt_input_to_output")
        self.decrypt_input_to_file = QAction(MainWindow)
        self.decrypt_input_to_file.setObjectName(u"decrypt_input_to_file")
        self.main_widget = QWidget(MainWindow)
        self.main_widget.setObjectName(u"main_widget")
        self.verticalLayout = QVBoxLayout(self.main_widget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gb_settings = QGroupBox(self.main_widget)
        self.gb_settings.setObjectName(u"gb_settings")
        self.gridLayout = QGridLayout(self.gb_settings)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lb_password = QLabel(self.gb_settings)
        self.lb_password.setObjectName(u"lb_password")

        self.gridLayout.addWidget(self.lb_password, 0, 0, 1, 1)

        self.le_password = QLineEdit(self.gb_settings)
        self.le_password.setObjectName(u"le_password")
        self.le_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.le_password, 0, 1, 1, 1)

        self.cb_show_password = QCheckBox(self.gb_settings)
        self.cb_show_password.setObjectName(u"cb_show_password")

        self.gridLayout.addWidget(self.cb_show_password, 0, 2, 1, 1)

        self.hs_1 = QSpacerItem(273, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.hs_1, 0, 3, 1, 1)

        self.lb_filename = QLabel(self.gb_settings)
        self.lb_filename.setObjectName(u"lb_filename")

        self.gridLayout.addWidget(self.lb_filename, 1, 0, 1, 1)

        self.le_filename = QLineEdit(self.gb_settings)
        self.le_filename.setObjectName(u"le_filename")

        self.gridLayout.addWidget(self.le_filename, 1, 1, 1, 3)


        self.verticalLayout.addWidget(self.gb_settings)

        self.gb_input = QGroupBox(self.main_widget)
        self.gb_input.setObjectName(u"gb_input")
        self.horizontalLayout_4 = QHBoxLayout(self.gb_input)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.te_input = MyPlainTextEdit(self.gb_input)
        self.te_input.setObjectName(u"te_input")
        font = QFont()
        font.setFamilies([u"Courier New"])
        font.setPointSize(10)
        self.te_input.setFont(font)

        self.horizontalLayout_4.addWidget(self.te_input)


        self.verticalLayout.addWidget(self.gb_input)

        self.hl_buttons = QHBoxLayout()
        self.hl_buttons.setSpacing(6)
        self.hl_buttons.setObjectName(u"hl_buttons")
        self.hl_buttons.setContentsMargins(6, -1, 6, -1)
        self.pb_encrypt_from_file = QPushButton(self.main_widget)
        self.pb_encrypt_from_file.setObjectName(u"pb_encrypt_from_file")

        self.hl_buttons.addWidget(self.pb_encrypt_from_file)

        self.pb_decrypt_to_file = QPushButton(self.main_widget)
        self.pb_decrypt_to_file.setObjectName(u"pb_decrypt_to_file")

        self.hl_buttons.addWidget(self.pb_decrypt_to_file)

        self.hs_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_buttons.addItem(self.hs_2)

        self.pb_encrypt = QPushButton(self.main_widget)
        self.pb_encrypt.setObjectName(u"pb_encrypt")

        self.hl_buttons.addWidget(self.pb_encrypt)

        self.pb_decrypt = QPushButton(self.main_widget)
        self.pb_decrypt.setObjectName(u"pb_decrypt")

        self.hl_buttons.addWidget(self.pb_decrypt)


        self.verticalLayout.addLayout(self.hl_buttons)

        self.gb_output = QGroupBox(self.main_widget)
        self.gb_output.setObjectName(u"gb_output")
        self.horizontalLayout_5 = QHBoxLayout(self.gb_output)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.te_output = QPlainTextEdit(self.gb_output)
        self.te_output.setObjectName(u"te_output")
        self.te_output.setFont(font)
        self.te_output.setAcceptDrops(False)
        self.te_output.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.te_output)


        self.verticalLayout.addWidget(self.gb_output)

        MainWindow.setCentralWidget(self.main_widget)
        self.menu_bar = QMenuBar(MainWindow)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 639, 33))
        self.menu_file = QMenu(self.menu_bar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_help = QMenu(self.menu_bar)
        self.menu_help.setObjectName(u"menu_help")
        self.menu_encrypt = QMenu(self.menu_bar)
        self.menu_encrypt.setObjectName(u"menu_encrypt")
        self.menu_decrypt = QMenu(self.menu_bar)
        self.menu_decrypt.setObjectName(u"menu_decrypt")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.menu_bar.addAction(self.menu_file.menuAction())
        self.menu_bar.addAction(self.menu_encrypt.menuAction())
        self.menu_bar.addAction(self.menu_decrypt.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.file_new)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.file_exit)
        self.menu_help.addAction(self.help_about)
        self.menu_encrypt.addAction(self.encrypt_input_to_output)
        self.menu_encrypt.addAction(self.encrypt_file_to_output)
        self.menu_decrypt.addAction(self.decrypt_input_to_output)
        self.menu_decrypt.addAction(self.decrypt_input_to_file)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"crippy", None))
        self.file_exit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
#if QT_CONFIG(shortcut)
        self.file_exit.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+F4", None))
#endif // QT_CONFIG(shortcut)
        self.help_about.setText(QCoreApplication.translate("MainWindow", u"A&bout", None))
#if QT_CONFIG(shortcut)
        self.help_about.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+B", None))
#endif // QT_CONFIG(shortcut)
        self.file_open.setText(QCoreApplication.translate("MainWindow", u"Open (to Input)", None))
#if QT_CONFIG(shortcut)
        self.file_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.file_save.setText(QCoreApplication.translate("MainWindow", u"Save (from Output)", None))
#if QT_CONFIG(shortcut)
        self.file_save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.file_new.setText(QCoreApplication.translate("MainWindow", u"&New", None))
#if QT_CONFIG(shortcut)
        self.file_new.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.encrypt_input_to_output.setText(QCoreApplication.translate("MainWindow", u"Input -> Output", None))
        self.encrypt_file_to_output.setText(QCoreApplication.translate("MainWindow", u"File -> Output", None))
        self.decrypt_input_to_output.setText(QCoreApplication.translate("MainWindow", u"Input -> Output", None))
        self.decrypt_input_to_file.setText(QCoreApplication.translate("MainWindow", u"Input -> File", None))
        self.gb_settings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.lb_password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.le_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"enter password...", None))
        self.cb_show_password.setText(QCoreApplication.translate("MainWindow", u"Show password", None))
        self.lb_filename.setText(QCoreApplication.translate("MainWindow", u"Filename:", None))
        self.gb_input.setTitle(QCoreApplication.translate("MainWindow", u"Input", None))
        self.te_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nothing to show here...", None))
        self.pb_encrypt_from_file.setText(QCoreApplication.translate("MainWindow", u"Encrypt from File", None))
        self.pb_decrypt_to_file.setText(QCoreApplication.translate("MainWindow", u"Decrypt to File", None))
        self.pb_encrypt.setText(QCoreApplication.translate("MainWindow", u"Encrypt", None))
        self.pb_decrypt.setText(QCoreApplication.translate("MainWindow", u"Decrypt", None))
        self.gb_output.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
        self.te_output.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nothing to show here...", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.menu_encrypt.setTitle(QCoreApplication.translate("MainWindow", u"Encrypt", None))
        self.menu_decrypt.setTitle(QCoreApplication.translate("MainWindow", u"Decrypt", None))
    # retranslateUi

