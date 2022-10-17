import datetime
import sys
import os
import time
import configparser
from dateutil.relativedelta import relativedelta

sys.path.insert(1, "../")
sys.path.insert(1, "./viewports")
sys.path.insert(1, "./objects")
from objects.klassen import *
from objects.datev import *
from objects import datenbank as db

from libs.log import *
import concurrent.futures
from PyQt5.QtWidgets import QApplication, QInputDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtCore import Qt
import hashlib

# UI elements (viewports)
from gui.viewports.login import Ui_MainWindow as login
from gui.viewports.mainmenu import Ui_MainWindow as mainmenu
from gui.viewports.conflicts import Ui_MainWindow as conflict
from gui.viewports.order import Ui_MainWindow as order
from gui.viewports.order_lineitem import Ui_MainWindow as order_lineitem
from gui.viewports.warehouse import Ui_MainWindow as warehouse
from gui.viewports.customers import Ui_MainWindow as customer


#####################################################
#   MainWindow handles main functionality of gui    #
#   >>  viewport swaps                              #
#   >>  login / logout                              #
#####################################################


class MainWindow:
    def __init__(self, session):
        self.main_win = QMainWindow()
        self.session = session
        self.log = Logger("syslog", "functional_gui", str(self.session.user.benutzer))
        self.show_login()  # In der Session werden alle Objekte gespeichert
        self.windowshistory = []

    def show(self):
        self.main_win.show()

    def show_login(self):
        try:
            self.log.info("show window: login")
            self.ui = login()
            self.ui.setupUi(self.main_win)
        except Exception as e:
            self.log.error("show_login: " + str(e))
            self.log.critical(
                "show_login: window can't be rendered. EXIT program due to crit"
            )
        try:
            # hooks login
            self.ui.button_login.clicked.connect(self.login)

        except Exception as e:
            self.log.error("show_login: " + str(e))

    def show_mainmenu(self):
        try:
            self.log.info("show window: mainmenu")
            self.ui = mainmenu()
            self.ui.setupUi(self.main_win)
            self.windowshistory.append(self.show_mainmenu)
        except Exception as e:
            self.log.error("show_mainmenu: " + str(e))
            self.show_login()
        try:
            # hooks mainmenu
            self.ui.button_menu_customer.clicked.connect(self.show_customer)
            self.ui.button_menu_article.clicked.connect(self.show_warehouse)
            self.ui.button_menu_order.clicked.connect(self.show_order)
            self.ui.button_menu_rules.clicked.connect(self.show_conflict)
            self.ui.button_menu_logout.clicked.connect(self.logout)
        except Exception as e:
            self.log.error("show_mainmenu: " + str(e))

    def show_customer(self):
        try:
            self.log.info("show window: customer")
            self.ui = customer()
            self.ui.setupUi(self.main_win)
            self.windowshistory.append(self.show_customer)
        except Exception as e:
            self.log.error("show_customer: " + str(e))
            self.show_mainmenu()
        try:
            # hooks customer
            self.ui.button_customer_back.clicked.connect(self.back)
            self.ui.button_customer_newCustomer.clicked.connect(self.save_kunden)
            self.ui.button_customer_deleteCustomer.clicked.connect(self.delete_kunden)
            self.ui.button_customer_showOrders.clicked.connect(
                lambda: self.show_order(self.ui.input_customer_customerId.text())
            )
            self.ui.button_customer_showProject.clicked.connect(
                lambda: self.show_order(self.ui.input_customer_customerId.text(), True)
            )
            self.ui.listWidget_customer_search.itemClicked.connect(self.show_kunden)
            self.ui.input_customer_search.returnPressed.connect(self.search_kunden)
            self.ui.button_customer_searchGo.clicked.connect(self.search_kunden)
            self.ui.input_customer_customerId.textChanged.connect(
                lambda: self.change_name_newcustomer_button(
                    self.ui.input_customer_customerId.text()
                )
            )
            self.ui.button_customer_clear.clicked.connect(
                lambda: self.show_kunden(True, True)
            )
            self.search_kunden()
        except Exception as e:
            self.log.error("show_customer: " + str(e))

    def show_order(self, search=None, search_konfiguration=False):
        try:
            self.log.info("show window: order")
            self.ui = order()
            self.ui.setupUi(self.main_win)
            self.windowshistory.append(self.show_order)
        except Exception as e:
            self.log.error("show_order: " + str(e))
            self.show_mainmenu()
        try:
            # hooks customer
            self.ui.button_order_back.clicked.connect(self.back)
            self.ui.button_order_addLineItem.clicked.connect(
                self.show_positionen_bestellung
            )
            self.ui.button_order_newOrder.clicked.connect(self.save_bestellung)
            self.ui.button_order_deleteorder.clicked.connect(self.delete_bestellungen)
            self.ui.input_order_search.returnPressed.connect(self.search_bestellungen)
            self.ui.listView_order_searchlist.itemClicked.connect(self.show_bestellung)
            self.ui.button_order_datevExport.clicked.connect(self.datev_export)
            self.ui.button_order_searchGo.clicked.connect(self.search_bestellungen)
            self.ui.button_order_clear.clicked.connect(
                lambda: self.show_bestellung(True, True)
            )
            self.ui.input_order_orderId.textChanged.connect(
                lambda: self.change_name_neworder_button(
                    self.ui.input_order_orderId.text()
                )
            )
            if search:
                self.search_bestellungen(search, search_konfiguration)
            else:
                self.search_bestellungen()

        except Exception as e:
            self.log.error("show_order: " + str(e))

    def show_order_lineitem(self):
        try:
            self.log.info("show window: lineitem")
            self.ui = order_lineitem()
            self.ui.setupUi(self.main_win)
            self.windowshistory.append(self.show_order_lineitem)
        except Exception as e:
            self.log.error("show_order_lineitem: " + str(e))
            self.show_mainmenu()
        try:
            # hooks customer
            self.ui.button_orderlineitem_back.clicked.connect(
                self.from_position_to_bestellung
            )
            self.ui.button_orderlineitem_newOrderlineitem.clicked.connect(
                self.add_position
            )
            self.ui.button_orderlineitem_deleteLine.clicked.connect(
                self.delete_positionen
            )
            self.ui.button_orderlineitem_saveLine.clicked.connect(self.save_positionen)
            self.create_dropdown_position()
            self.ui.listWidget_orderlineitem_lineitemlist.itemClicked.connect(
                self.show_position
            )
            self.ui.dropdown_orderlineitem_Article.currentIndexChanged.connect(
                self.show_price_positionen
            )
            self.ui.button_orderlineitem_clear.clicked.connect(self.clear_position)
        except Exception as e:
            self.log.error("show_order_lineitem: " + str(e))

    def show_warehouse(self):
        try:
            self.log.info("show window: warehouse")
            self.ui = warehouse()
            self.ui.setupUi(self.main_win)
            self.windowshistory.append(self.show_warehouse)
        except Exception as e:
            self.log.error("show_warehouse: " + str(e))
            self.show_mainmenu()
        try:
            # hooks customer
            self.ui.button_warehouse_back.clicked.connect(self.back)
            self.ui.button_warehouse_newArticle.clicked.connect(self.save_artikel)
            self.ui.button_warehouse_deleteArticle.clicked.connect(self.delete_artikel)
            self.ui.input_warehouse_search.returnPressed.connect(self.search_artikel)
            self.ui.button_warehouse_searchGo.clicked.connect(self.search_artikel)
            self.ui.listView_warehouse_search.itemClicked.connect(self.show_artikel)
            self.ui.button_warehouse_deleteArticle_2.clicked.connect(
                self.artikel_show_conflict
            )
            self.ui.button_warehouse_newCategory.clicked.connect(self.show_dialoge)
            self.ui.input_warehouse_articleId.textChanged.connect(
               lambda: self.change_name_newarticle_button(
                  self.ui.input_warehouse_articleId.text()
               )
            )
            self.ui.button_warehouse_clear.clicked.connect(
                lambda: self.show_artikel(True, True)
            )
            self.kategorie()
            self.search_artikel()
        except Exception as e:
            self.log.error("show_warehouse: " + str(e))

    def show_conflict(self):
        try:
            self.log.info("show window: conflict")
            self.ui = conflict()
            self.ui.setupUi(self.main_win)
            self.windowshistory.append(self.show_conflict)
        except Exception as e:
            self.log.error("show_conflict: " + str(e))
            self.show_mainmenu()
        try:
            # hooks customer
            self.ui.button_conflicts_back.clicked.connect(self.back)
            self.ui.button_conflicts_newConflict.clicked.connect(self.add_konflikte)
            self.ui.button_conflicts_deleteConflict.clicked.connect(
                self.delete_konflikte
            )
            # self.ui.button_conflicts_saveConflict.clicked.connect(self.logout)
            self.create_dropdown_konflikte()
            self.ui.input_conflicts_articleId.currentIndexChanged.connect(
                self.show_konflikte
            )

        except Exception as e:
            self.log.error("show_conflict: " + str(e))

    #####################################################################
    ## functional part begins here ######################################
    #####################################################################

    def error_fallback(self):
        # if self.session.user.benutzer:
        # self.show_mainmenu()
        # else:
        # self.show_login()
        self.messagebox(
            "ERROR",
            "Ein Unbekannter Fehler ist aufgetreten. Wenden Sie sich an den Administrator",
        )

    def back(self):
        self.windowshistory.pop()
        self.windowshistory.pop()()

    def change_name_newcustomer_button(self, inputtext):
        if inputtext == "" or inputtext == None or inputtext == "None":
            return
        try:
            int(inputtext)
        except:
            return

        connection = db.create_connection()
        result = db.select_from_database(
            connection,
            "select KundenID from kunden where KundenID = " + str(int(inputtext)),
        )
        if result[0]:
            self.ui.button_customer_newCustomer.setText("Änderung speichern")
            if inputtext != self.ui.input_customer_search.text():
                self.ui.input_customer_search.setText(str(inputtext))

        else:
            self.ui.button_customer_newCustomer.setText("Neuer Kunde")

    def change_name_neworder_button(self, inputtext):
        if inputtext == "" or inputtext == None or inputtext == "None":
            return
        try:
            int(inputtext)
        except:
            return

        connection = db.create_connection()
        result = db.select_from_database(
            connection,
            "select BestellungID from bestellung where BestellungID = "
            + str(int(inputtext)),
        )
        if result[0]:
            self.ui.button_order_newOrder.setText("Änderung speichern")
            if inputtext != self.ui.input_order_search.text():
                self.ui.input_order_search.setText(str(inputtext))

        else:
            self.ui.button_order_newOrder.setText("Neue Bestellung")

    def change_name_newarticle_button(self, inputtext):
        if inputtext == "" or inputtext == None or inputtext == "None":
            return
        try:
            int(inputtext)
        except:
            return

        if inputtext == "":
            return
        connection = db.create_connection()
        result = db.select_from_database(
            connection,
            "select ProduktID from produkte where ProduktID = " + str(int(inputtext)),
        )
        if result[0]:
            self.ui.button_warehouse_newArticle.setText("Änderung speichern")
            if inputtext != self.ui.input_warehouse_search.text():
                self.ui.input_warehouse_search.setText(str(inputtext))

        else:
            self.ui.button_warehouse_newArticle.setText("Neuer Artikel")


    def set_order_by_ID(self, inputtext):
        if inputtext == "" or inputtext == None or inputtext == "None":
            return False
        try:
            int(inputtext)
        except:
            return False

        connection = db.create_connection()
        result = db.select_from_database(
            connection,
            "select BestellungID from bestellung where BestellungID = " + str(int(inputtext)),
        )
        if result[0]:
                self.ui.input_order_search.setText(str(inputtext))
                self.search_bestellungen()
                return True

        else:
            return False

    def get_orders_by_month(self, month):
        try:
            orders = []
            filtered_orders = []
            connection = db.create_connection()
            dbdata = db.select_from_database(connection, "select * from bestellung")
            this_month = datetime.date.today() - datetime.timedelta(
                days=datetime.date.today().day
            )
            this_month = this_month - relativedelta(months=month)
            last_month = this_month - relativedelta(months=1)

            for order in dbdata:
                try:
                    orders.append(
                        Bestellungen(
                            order["BestellungID"],
                            order["KundenID"],
                            order["Datum"],
                            order["Bestellsumme"],
                            order["Bezahlt"],
                            order["Bezahlt_am"],
                            order["hilfe"],
                        )
                    )
                except Exception as e:
                    print(e)

            oldest_order = this_month

            for order in orders:
                if order.datum.date() < oldest_order:
                    oldest_order = order.datum.date()
                if order.datum.date() < this_month and order.datum.date() >= last_month:
                    filtered_orders.append(order)

            return filtered_orders, oldest_order
        except Exception as e:
            self.log.error("get_orders_by_month: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def datev_export(self):
        try:

            exported_months = []
            last_month_is_allready_exported = False

            # read config 4 Datev data
            try:
                Config = configparser.ConfigParser()
                Config.read("config.ini")
                absenderID = str(Config.get("DATEV-export", "absenderID"))
                Kodierung = str(Config.get("DATEV-export", "Kodierung"))
                speicherort = str(Config.get("DATEV-export", "Speicherort"))
            except Exception as e:
                log.error(
                    "datev_exporter: Config.ini nicht auffindbar oder nicht lesbar: "
                    + str(e)
                )
                self.messagebox(
                    "Fehler",
                    "DATEV Export Fehlgeschlagen",
                    "Voreinstellungen aus config.ini konten nicht gelesen werden",
                )
                return False

            try:
                self.get_orders_by_month(1)
            except Exception as e:
                print(e)

            # check for directory to avoid errors
            if not os.path.isdir(speicherort):
                log.warn(
                    "datev_exporter: Speicherort nicht vorhanden. Ordner wird angelegt."
                )
                os.mkdir(speicherort)

            # initialize DATEV exporter with config data
            try:
                exporter = DatevExporter(absenderID, Kodierung, speicherort)
            except Exception as e:
                log.error("datev_exporter: Config Daten fehlerhaft: " + str(e))
                self.messagebox(
                    "Fehler",
                    "DATEV Export Fehlgeschlagen",
                    "Die Voreinstellungen aus config.ini scheinen fehlerhaft zu sein!",
                )

            # get current month & year and get the date of the oldest order in the DB.
            this_month = datetime.date.today() - datetime.timedelta(
                days=datetime.date.today().day
            )
            waste, oldestmonth = self.get_orders_by_month(0)

            # for max. last 12 month >> export DATEV.txt if not there yet
            for i in range(12):
                this_month = this_month - relativedelta(months=1)
                filename = str(this_month.year) + "-" + str(this_month.month)

                # break at oldest order to avoid iterating through all 12 months.
                if oldestmonth > this_month - relativedelta(months=i):
                    self.log.info(
                        "datev_export: stop at "
                        + str(oldestmonth)
                        + " beacuse its the oldest order"
                    )
                    break

                # if month wasn't exported yet >> export it
                if not exists(speicherort + filename + ".txt"):
                    exporter.buchungsstapel.clear()
                    monthorders, waste = self.get_orders_by_month(i)
                    if len(monthorders) != 0:
                        for order in monthorders:
                            exporter.buchungsstapel.add_buchung(
                                order.bestellsumme, order.datum.date(), order.id
                            )
                        exporter.export(filename)
                        exported_months.append(filename)
                        if i == 0:
                            last_month_is_allready_exported = True
                    else:
                        self.log.smallwarn(
                            "datev_export: keine Buchungsdaten zu diesem Monat gefunden: "
                            + str(filename)
                        )

            self.log.info("datev_export: done")

            # User Output
            if len(exported_months) != 0:
                self.messagebox(
                    "DATEX Export",
                    "Export erfolgreich abgeschlossen!",
                    "folgende Monate wurden exportiert: \n"
                    + str(exported_months).replace("[", "").replace("]", "")
                    + "\n\n Sie sind im Ordner "
                    + speicherort
                    + " zu finden.",
                    QMessageBox.Information,
                )
                path = os.path.realpath(speicherort)
                os.startfile(path)
            else:
                self.messagebox(
                    "DATEX Export",
                    "Keine Daten Exportiert",
                    "Alle vergangenen Monate wurde bereits exportiert. Lösche einen Export im Order '"
                    + speicherort
                    + "' um ihn erneut zu exportieren.",
                    QMessageBox.Information,
                )

        except Exception as e:
            self.log.error("datev_export: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def search_kunden(self):
        try:
            """
            Implementiert Suchfunktion für Kunden
            :return:
            """
            self.session.kunden.search(self.ui.input_customer_search.text())
            self.log.info(
                "search_kunden: searching " + str(self.ui.input_customer_search.text())
            )
            self.ui.listWidget_customer_search.clear()
            self.ui.listWidget_customer_search.addItems(
                self.session.kunden.get_label_list()
            )
            self.log.info("search_kunden: search done")

        except Exception as e:
            self.log.error("search_kunden: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def show_kunden(self, useless=False, clear=False):
        try:
            """
            Methode implementiert die Möglichkeit, die Felder mit den Datensatzeinträgen zu füllen
            :return:
            """

            if clear:
                emptyCustomer = Kunde()
                self.session.kunden.liste.insert(0, emptyCustomer)
                self.session.kunden.set_current(0)
            else:
                self.session.kunden.set_current(
                    self.ui.listWidget_customer_search.currentRow()
                )

            self.ui.input_customer_customerId.setText(
                str(self.session.kunden.get_current().id)
            )
            self.ui.input_customer_lastname.setText(
                str(self.session.kunden.get_current().nachname or "")
            )
            self.ui.input_customer_firsname.setText(
                str(self.session.kunden.get_current().name or "")
            )
            self.ui.input_customer_city.setText(
                str(self.session.kunden.get_current().ort or "")
            )
            self.ui.input_customer_zip.setText(
                str(self.session.kunden.get_current().plz or "")
            )
            self.ui.input_customer_street.setText(
                str(self.session.kunden.get_current().strasse or "")
            )
            self.ui.input_customer_streetnumber.setText(
                str(self.session.kunden.get_current().hausnummer or "")
            )
            self.ui.input_customer_mail.setText(
                str(self.session.kunden.get_current().e_mail or "")
            )
            self.ui.dateEdit_customer_birthday.setDate(
                self.session.kunden.get_current().geburtsdatum
            )
            self.ui.input_customer_company.setText(
                str(self.session.kunden.get_current().firma or "")
            )
            self.ui.checkBox_customer_isCompany.setChecked(
                self.session.kunden.get_current().heandler == 1
            )
            self.log.info(
                "show_kunden: loaded customer: "
                + str(self.session.kunden.get_current().id)
            )

        except Exception as e:
            self.log.error("show_kunden: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def messagebox(self, title, heading, message="", icon=QMessageBox.Warning):
        try:
            msg = QMessageBox()  # new instance to reset all out/inputs
            msg.setIcon(icon)
            msg.setText(str(heading))
            msg.setInformativeText(str(message))
            msg.setWindowTitle(str(title))
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        except Exception as e:
            self.log.error("Message Box: Unbekannter Fehler: " + str(e))

    def show_dialoge(self):

        try:
            a = QInputDialog()
            a.setLabelText("Neue Kategorie")
            a.setTextValue("....")
            a.setOkButtonText("save")

            a.exec_()

            ausgabe = datenbank.send_to_database(
                datenbank.create_connection(),
                "insert into produktkategorie(Produkt_Bezeichnung) Values(?)",
                (str(a.textValue()),),
            )

            if not ausgabe:
                self.messagebox(
                    "Datenbank-Fehler", "Kategorie konnte nicht erstellt werden"
                )
            else:

                self.session.artikel.update()
                self.kategorie()

        except Exception as e:
            self.log.error("Message Box: Unbekannter Fehler: " + str(e))

    def login(self):
        try:
            if self.session.user.login(
                self.ui.input_login_username.text(),
                self.ui.input_login_password.text(),
            ):
                self.log.info("user logged in: " + str(self.session.user.benutzer))
                self.show_mainmenu()
            else:
                self.messagebox("Login-Fehler", "Nutzername oder Passwort falsch")
                self.log.warn("login: Login-Fehler Nutzername oder Passwort falsch")

        except Exception as e:
            self.log.error("login: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def logout(self):
        try:
            self.log.info("user logged out: " + str(self.session.user.benutzer))
            self.show_login()
        except Exception as e:
            self.log.error("logout: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def save_kunden(self):
        """
        Implementiert Speichermöglichkeit für das Kunden-GUI
        :return:
        """
        try:
            if (
                self.ui.input_customer_customerId.text() == ""
                or self.ui.input_customer_customerId.text() == None
            ):
                self.messagebox("Input-Fehler", "Keine ID eingegeben")
                self.log.warn("save_kunden: Input-Fehler Keine ID eingegeben")
                return

            self.session.kunden.save(
                self.ui.input_customer_customerId.text(),
                self.ui.input_customer_firsname.text(),
                self.ui.input_customer_lastname.text(),
                self.ui.dateEdit_customer_birthday.dateTime().toPyDateTime(),
                self.ui.input_customer_zip.text(),
                self.ui.input_customer_city.text(),
                self.ui.input_customer_mail.text(),
                self.ui.input_customer_street.text(),
                self.ui.input_customer_streetnumber.text(),
                self.ui.checkBox_customer_isCompany.isChecked(),
                self.ui.input_customer_company.text(),
            )
            self.search_kunden()
            self.log.info("save_kunden: saved customer")

        except Exception as e:
            self.log.error("save_kunden: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def delete_kunden(self):
        """
        Implementiert die Möglichkeit im Kunden GUI Einträge zu löschen.

        :return:
        """
        try:
            if self.ui.listWidget_customer_search.currentRow() == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                self.log.warn("search customer: FEHLER kein Eintrag gewählt")
                return
            self.session.kunden.delete(self.ui.listWidget_customer_search.currentRow())
            self.search_kunden()
            self.log.info("delete_kunden: deleted customer")

        except Exception as e:
            self.log.error("delete_kunden: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def search_bestellungen(self, search=None, veri=False):
        """
        Implementiert Suchfunktion für Kunden
        :return:
        """
        try:
            self.session.bestellungen_search = self.ui.input_order_search.text()

            self.session.bestellungen.search(self.ui.input_order_search.text())
            self.log.info(
                "search_bestellungen: searching "
                + str(self.ui.input_order_search.text())
            )
            if search:
                self.session.bestellungen.search(str(search), str(search), veri)
            self.ui.listView_order_searchlist.clear()
            self.ui.listView_order_searchlist.addItems(
                self.session.bestellungen.get_label_list()
            )
            self.log.info("search_bestellungen: search done")

        except Exception as e:
            self.log.error("search_bestellungen: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def show_bestellung(self, useless=False, clear=False):
        try:
            if clear:
                emptyBestelleung = Bestellungen()
                self.session.bestellungen.liste.insert(0, emptyBestelleung)
                self.session.bestellungen_index = 0
            else:
                self.session.bestellungen_index = (
                    self.ui.listView_order_searchlist.currentRow()
                )

            self.session.bestellungen.set_current(self.session.bestellungen_index)
            self.ui.input_order_orderId.setText(
                str(self.session.bestellungen.get_current().id)
            )
            self.ui.input_order_priceIncVat.setText(
                "%.2f" % (self.session.bestellungen.get_current().bestellsumme * 1.19,)
            )
            self.ui.input_order_priceExVat.setText(
                "%.2f" % (self.session.bestellungen.get_current().bestellsumme,)
            )
            self.ui.checkbox_order_isConfiguration.setChecked(
                self.session.bestellungen.get_current().konfiguration
            )
            self.ui.checkbox_order_isPayed.setChecked(
                self.session.bestellungen.get_current().bezahlt
            )
            self.ui.input_order_customerID.setText(
                str(self.session.bestellungen.get_current().kunden_id)
            )
            self.ui.dateTimeEdit_order_paymentdate.setDate(
                self.session.bestellungen.get_current().bezahl_datum
            )
            self.ui.dateTimeEdit_order_orderdate.setDate(
                self.session.bestellungen.get_current().datum
            )
            self.ui.listView_order_lineitems.clear()
            self.ui.listView_order_lineitems.addItems(
                self.session.bestellungen.get_current().bestellpositionen.label_list
            )

            if clear:
                print("reset because True", clear)
                del self.session.bestellungen.liste[0]

        except Exception as e:
            self.log.error("show_bestellung: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def save_bestellung(self):

        try:
            if self.ui.input_order_orderId.text() == "":
                self.messagebox("Input-Fehler", "Keine ID eingegeben")
                self.log.warn("save_bestellung: Input-Fehler Keine ID eingegeben")
                return
            if self.ui.input_order_customerID.text() == "":
                self.messagebox("Input-Fehler", "Keine Kunden-ID eingegeben")
                self.log.warn("save_bestellung: Input-Fehler Keine ID eingegeben")
                return
            b = self.session.bestellungen.save(
                self.session,
                self.ui.input_order_orderId.text(),
                self.ui.input_order_customerID.text(),
                self.ui.dateTimeEdit_order_orderdate.dateTime().toPyDateTime(),
                self.ui.input_order_priceExVat.text(),
                self.ui.checkbox_order_isPayed.isChecked(),
                self.ui.dateTimeEdit_order_paymentdate.dateTime().toPyDateTime(),
                self.ui.checkbox_order_isConfiguration.isChecked(),
            )

            if self.ui.listView_order_searchlist.currentRow() != -1:
                self.session.bestellungen.get_current().bestellpositionen.add_to_other(
                    self.ui.input_order_orderId.text(),
                    self.ui.checkbox_order_isConfiguration.isChecked(),
                )

            if not b:
                self.messagebox("Input-Fehler", "Keine gültige Kunden-ID eingegeben")
                self.log.warn(
                    "save_bestellung: Input-Fehler Keine gültige Kunden-ID eingegeben"
                )

            self.search_bestellungen()
            self.log.info("save_bestellung: saved order")
        except Exception as e:
            self.log.error("save_bestellung: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def delete_bestellungen(self):
        try:
            if self.ui.input_order_orderId.text() == "":
                self.messagebox("Input-Fehler", "Keine ID eingegeben")
                self.log.warn(
                    "delete_bestellungen: Input-Fehler Keine gültige Kunden-ID eingegeben"
                )
                return
            self.session.bestellungen.delete(
                self.ui.input_order_orderId.text(),
                self.ui.checkbox_order_isConfiguration.isChecked(),
            )
            self.search_bestellungen()
            self.log.info("delete_bestellungen: deleted order")
        except Exception as e:
            self.log.error("delete_bestellungen: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def search_artikel(self):
        try:
            self.session.artikel.search(self.ui.input_warehouse_search.text())
            self.log.info(
                "search_artikel: searching "
                + str(self.ui.input_warehouse_search.text())
            )

            liste = self.session.artikel.get_label_list()
            self.ui.listView_warehouse_search.clear()

            for i in liste:

                item = QListWidgetItem(i[0])
                if i[1]:
                    item.setBackground(QColor("#eb4034"))

                self.ui.listView_warehouse_search.addItem(item)

            self.log.info("search_artikel: search done")

        except Exception as e:
            self.log.error("search_artikel: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def kategorie(self):

        try:
            for item in self.session.artikel.produktkategorie:
                self.ui.comboBox_warehouse_category.insertItem(item[0], item[2])
        except Exception as e:
            self.log.error("kategorie: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def clear_article(self):

        self.ui.input_warehouse_articleId.clear()

        self.ui.input_warehouse_articleName.clear()
        self.ui.input_warehouse_count_is.clear()
        self.ui.input_warehouse_storageId.clear()
        self.ui.input_warehouse_count_want.clear()
        self.ui.comboBox_warehouse_category.clear()
        self.ui.input_warehouse_price.clear()
        self.ui.listView.clear()

    def show_artikel(self, useless=False, clear=False):

        try:
            if clear:
                self.clear_article()
                return

            self.session.artikel.set_current(
                self.ui.listView_warehouse_search.currentRow()
            )

            self.ui.input_warehouse_articleId.setText(
                str(self.session.artikel.get_current().id)
            )
            self.ui.input_warehouse_articleName.setText(
                str(self.session.artikel.get_current().bezeichnung)
            )
            self.ui.input_warehouse_count_is.setText(
                str(self.session.artikel.get_current().bestand)
            )
            self.ui.input_warehouse_storageId.setText(
                str(self.session.artikel.get_current().lagerfach)
            )
            self.ui.input_warehouse_count_want.setText(
                str(self.session.artikel.get_current().meldebestand)
            )
            self.ui.comboBox_warehouse_category.setCurrentIndex(
                self.session.artikel.get_current().produktkatgorie_ID
            )
            self.ui.input_warehouse_price.setText(
                str(self.session.artikel.get_current().preis)
            )
            self.ui.listView.clear()
            self.ui.listView.addItems(
                self.session.konflikte.get_konflikte(
                    self.ui.input_warehouse_articleId.text()
                )
            )
        except Exception as e:
            self.log.error("show_artikel: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def artikel_show_conflict(self):
        try:
            if self.ui.input_warehouse_articleId.text() == "":
                self.messagebox("Input-Fehler", "Keine ID eingegeben")
                self.log.warn("artikel_show_conflict: Input-Fehler Keine ID eingegeben")
                return
            id = int(self.ui.input_warehouse_articleId.text())
            self.show_conflict()
            self.ui.input_conflicts_articleId.setCurrentIndex(
                self.session.konflikte.get_index_id(id)
            )
        except Exception as e:
            self.log.error("artikel_show_conflict: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def save_artikel(self):
        try:
            if self.ui.input_warehouse_articleId.text() == "":
                self.messagebox("Input-Fehler", "Keine ID eingegeben")
                self.log.warn("save_artikel: Input-Fehler Keine ID eingegeben")
                return
            if self.ui.input_warehouse_count_is.text() == "":
                self.messagebox("Input-Fehler", "Keine Menge eingegeben")
                self.log.warn("save_artikel: Input-Fehler Keine Menge eingegeben")
                return
            if self.ui.input_warehouse_count_want.text() == "":
                self.messagebox("Input-Fehler", "Keine Menge eingegeben")
                self.log.warn("save_artikel: Input-Fehler Keine Menge eingegeben")
                return
            self.session.artikel.save(
                self.ui.input_warehouse_articleId.text(),
                self.ui.input_warehouse_articleName.text(),
                self.ui.comboBox_warehouse_category.currentIndex(),
                self.ui.input_warehouse_price.text(),
                self.ui.input_warehouse_storageId.text(),
                int(float(self.ui.input_warehouse_count_is.text())),
                int(float(self.ui.input_warehouse_count_want.text())),
            )

            self.search_artikel()
            self.log.info("save_artikel: saved article")
        except Exception as e:
            self.log.error("save_artikel: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def delete_artikel(self):
        try:
            if self.ui.listView_warehouse_search.currentRow() == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                self.log.warn("delete_artikel: FEHLER kein Eintrag gewählt")
                return
            self.session.artikel.delete(self.ui.listView_warehouse_search.currentRow())
            self.session.artikel.update()
            self.search_artikel()

            self.log.info("delete_artikel: deleted article")
        except Exception as e:
            self.log.error("delete_artikel: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def create_dropdown_konflikte(self):
        try:
            self.session.konflikte.update()
            liste = self.session.konflikte.artikel_liste

            self.ui.input_conflicts_articleId.clear()

            for eintrag in liste:
                self.ui.input_conflicts_articleId.insertItem(eintrag[0], eintrag[1])
                self.ui.dropdown_conflicts_newConflictArticleName.insertItem(
                    eintrag[0], eintrag[1]
                )
        except Exception as e:
            self.log.error("create_dropdown_konflikte: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def show_konflikte(self):
        try:
            self.session.konflikte.search()
            id = self.ui.input_conflicts_articleId.currentIndex()
            self.session.konflikte.set_current(id)
            self.ui.listWidget_conflicts_conflictslist.clear()
            self.ui.listWidget_conflicts_conflictslist.addItems(
                self.session.konflikte.get_current().konflikte_name
            )
        except Exception as e:
            self.log.error("show_konflikte: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def add_konflikte(self):
        try:
            if (
                self.ui.dropdown_conflicts_newConflictArticleName.currentIndex()
                == self.ui.input_conflicts_articleId.currentIndex()
            ):
                self.messagebox("FEHLER", "kann sich nicht selber wählen")
                self.log.warn("add_konflikte: FEHLER kann sich nicht selber wählen")
                return
            if self.session.konflikte.index == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                self.log.warn("add_konflikte: FEHLER kein Eintrag gewählt")
                return

            b = self.session.konflikte.save(
                self.ui.dropdown_conflicts_newConflictArticleName.currentIndex()
            )
            if not b:
                self.messagebox("FEHLER", "Eintrag besteht schon")
                self.log.warn("add_konflikte: FEHLER Eintrag besteht schon")

            self.show_konflikte()
            self.log.info("add_konflikte: added conflict")
        except Exception as e:
            self.log.error("add_konflikte: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def delete_konflikte(self):
        try:


            if self.ui.listWidget_conflicts_conflictslist.currentRow() == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                self.log.warn("delete_konflikte: FEHLER kein Eintrag gewählt")
                return
            self.session.konflikte.delete(
                self.ui.listWidget_conflicts_conflictslist.currentRow()
            )
            self.show_konflikte()
            self.log.info("delete_konflikte: deleted conflict")
        except Exception as e:
            self.log.error("delete_konflikte: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def show_positionen_bestellung(self):
        try:

            if self.set_order_by_ID(self.ui.input_order_orderId.text()):
                self.ui.listView_order_searchlist.setCurrentRow(1)
                self.show_bestellung()

            if self.ui.listView_order_searchlist.currentRow() == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                return
            self.show_order_lineitem()
            self.ui.listWidget_orderlineitem_lineitemlist.addItems(
                self.session.bestellungen.get_current().bestellpositionen.label_list
            )
            self.ui.input_orderlineitem_orderId.setText(
                str(self.session.bestellungen.get_current().id)
            )

            self.session.bestellungen.get_current().bestellpositionen.update()
            self.ui.input_orderlineitem_totapriceExVat.setText(
                (
                    "%.2f"
                    % (
                        self.session.bestellungen.get_current().bestellpositionen.summeN,
                    )
                )
            )
            self.ui.input_orderlineitem_totapriceIclVat.setText(
                (
                    "%.2f"
                    % (
                        self.session.bestellungen.get_current().bestellpositionen.summeB,
                    )
                )
            )
        except Exception as e:
            self.log.error(
                "show_positionen_bestellung: Unbekannter Fehler >> " + str(e)
            )
            self.error_fallback()

    def show_position(self):
        try:
            index = self.ui.listWidget_orderlineitem_lineitemlist.currentRow()

            self.ui.input_order_singleitem_priceExVat.setText(
                str(
                    self.session.bestellungen.get_current().bestellpositionen.liste[
                        index
                    ][3]
                )
            )
            self.ui.input_orderlineitem_itemcount.setText(
                str(
                    self.session.bestellungen.get_current().bestellpositionen.liste[
                        index
                    ][2]
                )
            )

            for i, eintrag in enumerate(
                self.session.bestellungen.get_current().bestellpositionen.artikel_list
            ):
                if (
                    self.session.bestellungen.get_current().bestellpositionen.liste[
                        index
                    ][1]
                    == eintrag[0]
                ):
                    self.ui.dropdown_orderlineitem_Article.setCurrentIndex(i)
                    break
        except Exception as e:
            self.log.error("show_position: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def create_dropdown_position(self):
        try:
            self.session.bestellungen.get_current().bestellpositionen.update()
            liste = (
                self.session.bestellungen.get_current().bestellpositionen.artikel_list
            )

            for eintrag in liste:
                self.ui.dropdown_orderlineitem_Article.insertItem(
                    eintrag[0], eintrag[1]
                )
        except Exception as e:
            self.log.error("create_dropdown_position: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def add_position(self):
        try:
            if self.ui.input_orderlineitem_itemcount.text() == "":
                self.messagebox("FEHLER", "Keine Menge gewählt")
                self.log.warn("add_konflikte: FEHLER kKeine Menge gewählt")
                return
            index = self.ui.dropdown_orderlineitem_Article.currentIndex()
            b = self.session.bestellungen.get_current().bestellpositionen.add(
                index,
                self.ui.input_order_singleitem_priceExVat.text(),
                self.ui.input_orderlineitem_itemcount.text(),
            )
            if not b:
                self.messagebox("FEHLER", "Konflikt aufgetreten")
            else:
                self.update_gui_position()
        except Exception as e:
            self.log.error("add_position: Unbekannter Fehler >> " + str(e))
            self.error_fallback()


    def update_gui_position(self):
        try:
            self.ui.input_orderlineitem_totapriceExVat.setText(
                (
                    "%.2f"
                    % (
                        self.session.bestellungen.get_current().bestellpositionen.summeN,
                    )
                )
            )
            self.ui.input_orderlineitem_totapriceIclVat.setText(
                (
                    "%.2f"
                    % (
                        self.session.bestellungen.get_current().bestellpositionen.summeB,
                    )
                )
            )
            self.ui.listWidget_orderlineitem_lineitemlist.clear()
            self.ui.listWidget_orderlineitem_lineitemlist.addItems(
                self.session.bestellungen.get_current().bestellpositionen.label_list
            )

        except Exception as e:
            self.log.error("update_gui_position: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def show_price_positionen(self):
        try:
            self.ui.input_order_singleitem_priceExVat.setText(
                "%.2f"
                % (
                    self.session.bestellungen.get_current().bestellpositionen.artikel_list[
                        self.ui.dropdown_orderlineitem_Article.currentIndex()
                    ][
                        2
                    ],
                )
            )
        except Exception as e:
            self.log.error("show_price_positionen: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def delete_positionen(self):
        try:
            index = self.ui.listWidget_orderlineitem_lineitemlist.currentRow()

            if index == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                self.log.warn("delete_konflikte: FEHLER kein Eintrag gewählt")
                return

            self.session.bestellungen.get_current().bestellpositionen.delete(index)
            self.update_gui_position()
        except Exception as e:
            self.log.error("delete_positionen: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def save_positionen(self):
        try:
            index = self.ui.listWidget_orderlineitem_lineitemlist.currentRow()

            if index == -1:
                self.messagebox("FEHLER", "kein Eintrag gewählt")
                self.log.warn("delete_konflikte: FEHLER kein Eintrag gewählt")
                return

            indexart = self.ui.dropdown_orderlineitem_Article.currentIndex()
            b = self.session.bestellungen.get_current().bestellpositionen.save(
                indexart,
                self.ui.input_order_singleitem_priceExVat.text(),
                self.ui.input_orderlineitem_itemcount.text(),
                index,
            )
            if not b:
                self.messagebox("FEHLER", "Konflikt aufgetreten")
            else:
                self.update_gui_position()

        except Exception as e:
            self.log.error("save_positionen: Unbekannter Fehler >> " + str(e))
            self.error_fallback()

    def from_position_to_bestellung(self):
        try:
            self.show_order()
            self.windowshistory.pop()
            self.windowshistory.pop()
            self.ui.input_order_orderId.setText(
                str(self.session.bestellungen.get_current().id)
            )
            self.ui.input_order_priceIncVat.setText(
                "%.2f" % (self.session.bestellungen.get_current().bestellsumme * 1.19,)
            )
            self.ui.input_order_priceExVat.setText(
                "%.2f" % (self.session.bestellungen.get_current().bestellsumme,)
            )
            self.ui.checkbox_order_isConfiguration.setChecked(
                self.session.bestellungen.get_current().konfiguration
            )
            self.ui.checkbox_order_isPayed.setChecked(
                self.session.bestellungen.get_current().bezahlt
            )
            self.ui.input_order_customerID.setText(
                str(self.session.bestellungen.get_current().kunden_id)
            )
            self.ui.dateTimeEdit_order_paymentdate.setDate(
                self.session.bestellungen.get_current().bezahl_datum
            )
            self.ui.dateTimeEdit_order_orderdate.setDate(
                self.session.bestellungen.get_current().datum
            )
            self.ui.listView_order_lineitems.clear()
            self.ui.listView_order_lineitems.addItems(
                self.session.bestellungen.get_current().bestellpositionen.label_list
            )
            self.ui.listView_order_searchlist.setCurrentRow(
                self.session.bestellungen_index
            )
            self.ui.input_order_search.setText(self.session.bestellungen_search)

            self.search_bestellungen()
            self.save_bestellung()

        except Exception as e:
            self.log.error(
                "from_position_to_bestellung: Unbekannter Fehler >> " + str(e)
            )
            self.error_fallback()

    def clear_position(self):
        self.ui.input_order_singleitem_priceExVat.clear()
        self.ui.input_orderlineitem_itemcount.clear()


if __name__ == "__main__":
    session = Session()
    app = QApplication(sys.argv)
    main_win = MainWindow(session)
    main_win.show()
    sys.exit(app.exec_())
