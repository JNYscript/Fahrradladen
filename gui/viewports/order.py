# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './viewports/order.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 590)
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.0910909, y1:0.108, x2:1, y2:1, stop:0 rgba(15, 41, 46, 255), stop:1 rgba(26, 109, 117, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_order_search = QtWidgets.QLineEdit(self.centralwidget)
        self.input_order_search.setGeometry(QtCore.QRect(20, 20, 311, 33))
        self.input_order_search.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.input_order_search.setObjectName("input_order_search")
        self.listView_order_searchlist = QtWidgets.QListWidget(self.centralwidget)
        self.listView_order_searchlist.setGeometry(QtCore.QRect(20, 70, 371, 461))
        self.listView_order_searchlist.setStyleSheet("font: 57 14pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.listView_order_searchlist.setObjectName("listView_order_searchlist")
        self.input_order_orderId = QtWidgets.QLineEdit(self.centralwidget)
        self.input_order_orderId.setGeometry(QtCore.QRect(420, 20, 351, 33))
        self.input_order_orderId.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.input_order_orderId.setObjectName("input_order_orderId")
        self.input_order_priceExVat = QtWidgets.QLineEdit(self.centralwidget)
        self.input_order_priceExVat.setGeometry(QtCore.QRect(420, 164, 171, 33))
        self.input_order_priceExVat.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.input_order_priceExVat.setObjectName("input_order_priceExVat")
        self.button_order_deleteorder = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_deleteorder.setGeometry(QtCore.QRect(420, 540, 231, 41))
        self.button_order_deleteorder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_deleteorder.setStyleSheet("background-color: rgba(220, 100, 120, 150);\n"
"alternate-background-color: rgba(0, 0, 0, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.button_order_deleteorder.setObjectName("button_order_deleteorder")
        self.button_order_newOrder = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_newOrder.setGeometry(QtCore.QRect(190, 540, 201, 41))
        self.button_order_newOrder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_newOrder.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"alternate-background-color: rgba(0, 0, 0, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.button_order_newOrder.setObjectName("button_order_newOrder")
        self.button_order_back = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_back.setGeometry(QtCore.QRect(20, 540, 161, 41))
        self.button_order_back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_back.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"alternate-background-color: rgba(0, 0, 0, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.button_order_back.setObjectName("button_order_back")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 140, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Maven Pro")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(610, 140, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Maven Pro")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(420, 60, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Maven Pro")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_4.setObjectName("label_4")
        self.dateTimeEdit_order_orderdate = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_order_orderdate.setGeometry(QtCore.QRect(640, 90, 131, 31))
        self.dateTimeEdit_order_orderdate.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 50);\n"
"")
        self.dateTimeEdit_order_orderdate.setObjectName("dateTimeEdit_order_orderdate")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(640, 60, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Maven Pro")
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_6.setObjectName("label_6")
        self.input_order_priceIncVat = QtWidgets.QLineEdit(self.centralwidget)
        self.input_order_priceIncVat.setGeometry(QtCore.QRect(610, 164, 171, 33))
        self.input_order_priceIncVat.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.input_order_priceIncVat.setObjectName("input_order_priceIncVat")
        self.checkbox_order_isConfiguration = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_order_isConfiguration.setGeometry(QtCore.QRect(420, 444, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Maven Pro Medium")
        font.setPointSize(16)
        self.checkbox_order_isConfiguration.setFont(font)
        self.checkbox_order_isConfiguration.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
        self.checkbox_order_isConfiguration.setObjectName("checkbox_order_isConfiguration")
        self.checkbox_order_isPayed = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_order_isPayed.setGeometry(QtCore.QRect(420, 490, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Maven Pro Medium")
        font.setPointSize(16)
        self.checkbox_order_isPayed.setFont(font)
        self.checkbox_order_isPayed.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
        self.checkbox_order_isPayed.setObjectName("checkbox_order_isPayed")
        self.dateTimeEdit_order_paymentdate = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_order_paymentdate.setGeometry(QtCore.QRect(600, 490, 181, 31))
        self.dateTimeEdit_order_paymentdate.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 50);\n"
"")
        self.dateTimeEdit_order_paymentdate.setObjectName("dateTimeEdit_order_paymentdate")
        self.listView_order_lineitems = QtWidgets.QListWidget(self.centralwidget)
        self.listView_order_lineitems.setGeometry(QtCore.QRect(420, 240, 361, 191))
        self.listView_order_lineitems.setStyleSheet("font: 57 14pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.listView_order_lineitems.setObjectName("listView_order_lineitems")
        self.button_order_addLineItem = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_addLineItem.setGeometry(QtCore.QRect(740, 390, 41, 41))
        self.button_order_addLineItem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_addLineItem.setToolTipDuration(-1)
        self.button_order_addLineItem.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
"alternate-background-color: rgba(0, 0, 0, 50);\n"
"")
        self.button_order_addLineItem.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./gui\\edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_order_addLineItem.setIcon(icon)
        self.button_order_addLineItem.setIconSize(QtCore.QSize(25, 25))
        self.button_order_addLineItem.setObjectName("button_order_addLineItem")
        self.button_order_clear = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_clear.setGeometry(QtCore.QRect(660, 540, 121, 41))
        self.button_order_clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_clear.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"alternate-background-color: rgba(0, 0, 0, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.button_order_clear.setObjectName("button_order_clear")
        self.input_order_customerID = QtWidgets.QLineEdit(self.centralwidget)
        self.input_order_customerID.setGeometry(QtCore.QRect(420, 90, 171, 33))
        self.input_order_customerID.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.input_order_customerID.setReadOnly(False)
        self.input_order_customerID.setObjectName("input_order_customerID")
        self.button_order_searchGo = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_searchGo.setGeometry(QtCore.QRect(340, 20, 51, 33))
        self.button_order_searchGo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_searchGo.setStyleSheet("background-color: rgba(255, 255, 255, 50);\n"
"alternate-background-color: rgba(0, 0, 0, 50);\n"
"font: 57 16pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.button_order_searchGo.setObjectName("button_order_searchGo")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(420, 215, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Maven Pro")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_3.setObjectName("label_3")
        self.logo_login = QtWidgets.QLabel(self.centralwidget)
        self.logo_login.setGeometry(QtCore.QRect(190, 500, 31, 31))
        self.logo_login.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.logo_login.setText("")
        self.logo_login.setPixmap(QtGui.QPixmap("./gui\\datev.png"))
        self.logo_login.setScaledContents(True)
        self.logo_login.setObjectName("logo_login")
        self.button_order_datevExportlabel = QtWidgets.QLabel(self.centralwidget)
        self.button_order_datevExportlabel.setGeometry(QtCore.QRect(210, 500, 181, 31))
        self.button_order_datevExportlabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_datevExportlabel.setStyleSheet("background-color: rgba(134, 189, 65, 255);\n"
"alternate-background-color: rgba(134, 189, 65, 255);\n"
"font: 57 12pt \"Maven Pro Medium\";\n"
"color: rgb(255, 255, 255);")
        self.button_order_datevExportlabel.setTextFormat(QtCore.Qt.AutoText)
        self.button_order_datevExportlabel.setScaledContents(True)
        self.button_order_datevExportlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.button_order_datevExportlabel.setObjectName("button_order_datevExportlabel")
        self.button_order_datevExport = QtWidgets.QPushButton(self.centralwidget)
        self.button_order_datevExport.setGeometry(QtCore.QRect(190, 500, 201, 31))
        self.button_order_datevExport.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_order_datevExport.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"alternate-background-color: rgba(0, 0, 0, 0);\n"
"")
        self.button_order_datevExport.setText("")
        self.button_order_datevExport.setFlat(True)
        self.button_order_datevExport.setObjectName("button_order_datevExport")
        self.input_order_search.raise_()
        self.listView_order_searchlist.raise_()
        self.input_order_orderId.raise_()
        self.input_order_priceExVat.raise_()
        self.button_order_deleteorder.raise_()
        self.button_order_newOrder.raise_()
        self.button_order_back.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.dateTimeEdit_order_orderdate.raise_()
        self.label_6.raise_()
        self.input_order_priceIncVat.raise_()
        self.checkbox_order_isConfiguration.raise_()
        self.checkbox_order_isPayed.raise_()
        self.dateTimeEdit_order_paymentdate.raise_()
        self.listView_order_lineitems.raise_()
        self.button_order_addLineItem.raise_()
        self.button_order_clear.raise_()
        self.input_order_customerID.raise_()
        self.button_order_searchGo.raise_()
        self.label_3.raise_()
        self.button_order_datevExportlabel.raise_()
        self.logo_login.raise_()
        self.button_order_datevExport.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bestellungen"))
        self.input_order_search.setPlaceholderText(_translate("MainWindow", "Suche .."))
        self.input_order_orderId.setPlaceholderText(_translate("MainWindow", "Bestellnummer .."))
        self.input_order_priceExVat.setPlaceholderText(_translate("MainWindow", "Preis in € .."))
        self.button_order_deleteorder.setToolTip(_translate("MainWindow", "Strg + Entf"))
        self.button_order_deleteorder.setText(_translate("MainWindow", "Bestellung löschen"))
        self.button_order_deleteorder.setShortcut(_translate("MainWindow", "Ctrl+Del"))
        self.button_order_newOrder.setToolTip(_translate("MainWindow", "Strg + Enter"))
        self.button_order_newOrder.setText(_translate("MainWindow", "Neue Bestellung"))
        self.button_order_newOrder.setShortcut(_translate("MainWindow", "Ctrl+Return"))
        self.button_order_back.setToolTip(_translate("MainWindow", "Esc"))
        self.button_order_back.setText(_translate("MainWindow", "Zurück"))
        self.button_order_back.setShortcut(_translate("MainWindow", "Esc"))
        self.label.setText(_translate("MainWindow", "Gesamtpreis Netto"))
        self.label_2.setText(_translate("MainWindow", "Gesamtpreis Brutto"))
        self.label_4.setText(_translate("MainWindow", "Kunde"))
        self.label_6.setText(_translate("MainWindow", "Datum"))
        self.input_order_priceIncVat.setPlaceholderText(_translate("MainWindow", "Preis in € .."))
        self.checkbox_order_isConfiguration.setText(_translate("MainWindow", "ist Konfiguration"))
        self.checkbox_order_isPayed.setText(_translate("MainWindow", "ist Bezahlt"))
        self.button_order_addLineItem.setToolTip(_translate("MainWindow", "Str + P"))
        self.button_order_addLineItem.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.button_order_clear.setToolTip(_translate("MainWindow", "Strg + Rück (<--)"))
        self.button_order_clear.setText(_translate("MainWindow", "leeren"))
        self.button_order_clear.setShortcut(_translate("MainWindow", "Ctrl+Backspace"))
        self.input_order_customerID.setPlaceholderText(_translate("MainWindow", "Kunden ID"))
        self.button_order_searchGo.setToolTip(_translate("MainWindow", "Enter"))
        self.button_order_searchGo.setText(_translate("MainWindow", "Los"))
        self.button_order_searchGo.setShortcut(_translate("MainWindow", "Return"))
        self.label_3.setText(_translate("MainWindow", "Bestellpositionen"))
        self.button_order_datevExportlabel.setText(_translate("MainWindow", "DATEV Export   "))
        self.button_order_datevExport.setToolTip(_translate("MainWindow", "Strg + E"))
        self.button_order_datevExport.setShortcut(_translate("MainWindow", "Ctrl+E"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
