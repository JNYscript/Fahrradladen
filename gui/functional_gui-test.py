import sys

sys.path.insert(0, "../")
sys.path.insert(0, "./viewports")
import threading

import os
import time

# from libs import log #TODO add logs.py (MAX)
import concurrent.futures
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtCore import Qt
import hashlib

# UI elements (viewports)
from login import Ui_MainWindow as login
from mainmenu import Ui_MainWindow as mainmenu
from conflicts import Ui_MainWindow as conflict
from order import Ui_MainWindow as order
from order_lineitem import Ui_MainWindow as order_lineitem
from warehouse import Ui_MainWindow as warehouse
from customers import Ui_MainWindow as customer

#####################################################
#   MainWindow handles main functionality of gui    #
#   >>  viewport swaps                              #
#   >>  login / logout                              #
#####################################################


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.show_login()

    def show(self):
        self.main_win.show()

    def show_login(self):
        self.ui = login()
        self.ui.setupUi(self.main_win)
        # hooks login
        self.ui.button_login.clicked.connect(self.login)

    def show_mainmenu(self):
        self.ui = mainmenu()
        self.ui.setupUi(self.main_win)
        # hooks mainmenu
        self.ui.button_menu_customer.clicked.connect(self.show_customer)
        self.ui.button_menu_article.clicked.connect(self.show_warehouse)
        self.ui.button_menu_order.clicked.connect(self.show_order)
        self.ui.button_menu_rules.clicked.connect(self.show_conflict)
        self.ui.button_menu_logout.clicked.connect(self.logout)

    def show_customer(self):
        self.ui = customer()
        self.ui.setupUi(self.main_win)
        # hooks customer
        self.ui.button_customer_back.clicked.connect(self.show_mainmenu)
        # self.ui.button_customer_newCustomer.clicked.connect(self.show_mainmenu)
        # self.ui.button_customer_deleteCustomer.clicked.connect(self.show_mainmenu)
        # self.ui.button_customer_showOrders.clicked.connect(self.show_mainmenu)
        # self.ui.button_customer_showProject.clicked.connect(self.show_mainmenu)

    def show_order(self):
        self.ui = order()
        self.ui.setupUi(self.main_win)
        # hooks customer
        self.ui.button_order_back.clicked.connect(self.show_mainmenu)
        self.ui.button_order_addLineItem.clicked.connect(self.show_order_lineitem)
        # self.ui.button_order_newOrder.clicked.connect(self.show_mainmenu)
        # self.ui.button_order_deleteorder.clicked.connect(self.show_mainmenu)

    def show_order_lineitem(self):
        self.ui = order_lineitem()
        self.ui.setupUi(self.main_win)
        # hooks customer
        self.ui.button_orderlineitem_back.clicked.connect(self.show_order)
        # self.ui.button_orderlineitem_newOrderlineitem.clicked.connect(self.show_order_lineitem)
        # self.ui.button_orderlineitem_deleteLine.clicked.connect(self.show_mainmenu)
        # self.ui.button_orderlineitem_saveLine.clicked.connect(self.show_mainmenu)

    def show_warehouse(self):
        self.ui = warehouse()
        self.ui.setupUi(self.main_win)
        # hooks customer
        self.ui.button_warehouse_back.clicked.connect(self.show_mainmenu)
        # self.ui.button_warehouse_newArticle.clicked.connect(self.logout)
        # self.ui.button_warehouse_deleteArticle.clicked.connect(self.logout)

    def show_conflict(self):
        self.ui = conflict()
        self.ui.setupUi(self.main_win)
        # hooks customer
        self.ui.button_conflicts_back.clicked.connect(self.show_mainmenu)
        # self.ui.button_conflicts_newConflict.clicked.connect(self.logout)
        # self.ui.button_conflicts_deleteConflict.clicked.connect(self.logout)
        # self.ui.button_conflicts_saveConflict.clicked.connect(self.logout)

    #####################################################################
    ## functional part begins here ######################################
    #####################################################################

    def messagebox(self, title, heading, message=""):
        msg = QMessageBox()  # new instance to reset all out/inputs
        msg.setIcon(QMessageBox.Warning)
        msg.setText(str(heading))
        msg.setInformativeText(str(message))
        msg.setWindowTitle(str(title))
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    # TODO implement sql database connection to check login (JONAS)
    def checklogin(self, username, passhash):
        # passhash << "password"
        if (
            passhash
            == "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
            and username == "maddin"
        ):
            return True
        return False

    def login(self):
        if self.checklogin(
            self.ui.input_login_username.text(),
            hashlib.sha256(self.ui.input_login_password.text().encode()).hexdigest(),
        ):
            self.show_mainmenu()
        else:
            self.messagebox("Login-Fehler", "Nutzername oder Passwort falsch")

    def logout(self):
        self.show_login()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
