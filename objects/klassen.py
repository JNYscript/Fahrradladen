import sys

sys.path.insert(2, "..\\libs")
sys.path.insert(2, "..\\objects")

import datetime
import hashlib
import os
from libs.log import Logger

import objects.datenbank as datenbank
from objects.algorithmen import *

log = Logger("syslog", "klassen")


class Session:
    def __init__(self):
        self.connection = datenbank.create_connection()
        self.user = User(self.connection)
        self.kunden = KundenListe()
        self.bestellungen = BestellungListe()
        self.artikel = ArtikelListe()
        self.konflikte = KonfliktListe()
        self.bestellungen_search = ""
        self.bestellungen_index = -1


class User:
    def __init__(self, connection=None):
        self.benutzer = None
        self.connection = connection
        self.__verifiziert = False

    def is_verified(self):
        """
        gibt zurück ob User Verifiziert ist
        :return: bool
        """
        return self.__verifiziert

    def logout(self):
        """
        Funktion implementiert logout Funktion

        """
        self.benutzer = None
        self.__verifiziert = False

    def login(self, benutzer, passwort):
        """
        Funktion überprüft, ob eingegebene Login daten gültig sind.
        :param benutzer:
        :type benutzer:
        :param passwort:
        :type passwort:
        :return: Ob Login erfolgreich
        :rtype: boolean
        """
        connection = None
        if self.connection is None:
            connection = datenbank.create_connection()
        else:
            connection = self.connection

        statement = (
            f"""select salt,hash from verifikation where benutzername = '{benutzer}'"""
        )

        result = datenbank.select_from_database(connection, statement)

        if result[0] is None:
            return False

        login_passwort_hash = self.__create_hash(passwort, result[0]["salt"])

        if login_passwort_hash == result[0]["hash"]:
            self.benutzer = benutzer
            self.__verifiziert = True
            return True
        else:
            return False

    def create_user(self, benutzer, passwort):
        """
        Funktion registriert einen Benutzer
        :param benutzer:
        :type benutzer:
        :param passwort:
        :type passwort:
        :return: True wenn Registrierung erfolgreich, False + Fehlermeldung wenn nicht.
        :rtype: Boolean
        """
        salt = self.__create_salt()
        hash = self.__create_hash(passwort, salt)
        connection = None
        if self.connection is None:
            connection = datenbank.create_connection()
        else:
            connection = self.connection

        query = """INSERT INTO verifikation (benutzername,salt,hash) VALUES (?,?,?)"""

        values = (benutzer, salt, hash)

        result = datenbank.send_to_database(connection, query, values)
        if isinstance(result, str):

            log.error("Fehler aufgetreten: " + result)

            return False
        else:
            log.info("Nutzer erfolgreich registriert")
            return True

    def __create_salt(self):
        """
        Erstellt 32 bit Salt
        :return:
        :rtype: byte[]
        """
        return os.urandom(32)

    def __create_hash(self, passwort, salt):
        """
        Funktion erstellt einen Passwort-Hash aus passwort und salt
        :param passwort:
        :type passwort: String
        :param salt:
        :type salt:
        :return: gehashtes Passwort als Byte Array
        :rtype: byte[]
        """
        encoded_passwort = bytearray(passwort.encode("utf-8"))

        return hashlib.pbkdf2_hmac("sha256", encoded_passwort, salt, 100000)


class Artikel:

    # TODO
    def __init__(
        self,
        id=None,
        bezeichnung=None,
        produktkatgorie_ID=None,
        produktkategorie_name=None,
        preis=None,
        lagerfach=None,
        bestand=None,
        meldebestand=None,
    ):

        self.meldebestand = meldebestand
        self.bestand = bestand
        self.lagerfach = lagerfach
        self.preis = preis
        self.poduktkategorie_name = produktkategorie_name
        self.produktkatgorie_ID = produktkatgorie_ID
        self.bezeichnung = bezeichnung
        self.id = id
        self.label = f"{id}|{bezeichnung}"

        try:
            self.nachbestellen = bestand <= meldebestand
        except:
            self.nachbestellen = False


class Bestellungen:
    def __init__(
        self,
        id=None,
        kunden_id=None,
        datum=None,
        bestellsumme=None,
        bezahlt=None,
        bezahldatum=None,
        konfiguration=False,
        firma=None,
        name=None,
    ):

        self.konfiguration = konfiguration
        self.bezahlt = True if bezahlt == 1 else False
        self.bestellsumme = bestellsumme if bestellsumme is not None else 0
        self.kunden_id = kunden_id
        self.id = id

        self.datum = None
        self.bezahl_datum = None

        if datum is not None:
            self.datum = datetime.datetime(
                year=int(datum[0:4]), month=int(datum[5:7]), day=int(datum[8:10])
            )
        else:
            self.datum = datetime.datetime(year=1900, month=1, day=1)

        if bezahldatum is not None:
            self.bezahl_datum = datetime.datetime(
                year=int(bezahldatum[0:4]),
                month=int(bezahldatum[5:7]),
                day=int(bezahldatum[8:10]),
            )
        else:
            self.bezahl_datum = datetime.datetime(year=1900, month=1, day=1)

        a = "Konfiguration" if konfiguration else "Bestellung"

        # sql_result = datenbank.select_from_database()

        b = firma if firma is not None else name

        self.label = f"{id} | {a} | {b}"

        self.bestellpositionen = None
        if self.konfiguration:
            self.bestellpositionen = self.Konfigurationpositionen(self.id, self)
        else:
            self.bestellpositionen = self.Bestellpositionen(self.id, self)

    class Bestellpositionen:
        def __init__(self, id, bestellung):

            self.bestellung = bestellung
            self.sql_connector = datenbank.create_connection()
            self.liste = []
            self.id = id
            self.label_list = []
            self.artikel_list = []
            self.summeN = 0
            self.summeB = 0
            self.check_list = []
            self.update()

        def update(self):
            self.create_positionen_list()
            self.create_label_list()
            self._create_artikel_list()
            self.sum()
            self._create_chech_list()
            self.bestellung.bestellsumme = self.summeN

        def _create_artikel_list(self):

            liste = []

            sql = f"select ProduktID,Bezeichnung,Preis from produkte"

            result = datenbank.select_from_database(self.sql_connector, sql)

            for r in result:
                liste += [[r.get("ProduktID"), r.get("Bezeichnung"), r.get("Preis")]]

            self.artikel_list = liste

        def _get_artike(self, index):

            return self.artikel_list[index]

        def create_positionen_list(self):

            pos_list = []

            sql = f"""select Position,bestellungpos.ProduktID,Menge,bestellungpos.Preis,Summe,Bezeichnung from bestellungpos left join produkte p on p.ProduktID = bestellungpos.ProduktID where bestellungpos.BestellungID = {self.id}"""

            results = datenbank.select_from_database(self.sql_connector, sql)

            if results[0] is not None:
                for eintrag in results:
                    pos_list += [
                        [
                            eintrag.get("Position"),
                            eintrag.get("ProduktID"),
                            int(eintrag.get("Menge")),
                            eintrag.get("Preis"),
                            eintrag.get("Summe"),
                            eintrag.get("Bezeichnung"),
                        ]
                    ]

            self.liste = pos_list

        def create_label_list(self):

            self.label_list = []

            for row in self.liste:
                self.label_list += [f"{row[0]}|{row[5]}|{row[2]} stk.|{row[3]}€"]

        def sum(self):

            sum = 0

            for i in self.liste:
                sum += i[3] * i[2]

            self.summeN = sum
            self.summeB = sum * 1.19

        def get_new_id(self):

            if not self.liste:
                return 1

            for i in range(len(self.liste) - 1):
                if self.liste[1 + i][0] - self.liste[i][0] > 1:
                    return self.liste[i][0] + 1

            return self.liste[-1][0] + 1

        def delete(self, index):

            artikel = self.liste[index]

            slq = f"delete from bestellungpos where Position = ? and BestellungID = ? "
            values = (artikel[0], self.id)

            datenbank.send_to_database(self.sql_connector, slq, values)

            self.update()

        def add(self, index, preis, menge):

            sql = "insert into bestellungpos(BestellungID, Position,ProduktID, Menge, Preis, Summe) values(?,?,?,?,?,?)"

            artikel = self._get_artike(index)

            if artikel[0] in self.check_list:
                return False

            values = (
                self.id,
                self.get_new_id(),
                artikel[0],
                int(menge),
                float(preis),
                int(menge) * float(preis),
            )

            datenbank.send_to_database(self.sql_connector, sql, values)

            self.update()
            return True

        def save(self, index, preis, menge, index2):
            sql = f"""UPDATE bestellungpos 
                        set 
                        
                        ProduktID = ?,
                        Menge = ?,
                        Preis = ?,
                        Summe = ?
                        
                        where
                        
                        BestellungID = ?
                        
                        and
                        
                        Position = ?
                         """

            artikel = self._get_artike(index)

            if artikel[0] in self.check_list:
                return False

            values = (
                artikel[0],
                int(menge),
                float(preis),
                int(menge) * float(preis),
                self.id,
                self.liste[index2][0],
            )

            datenbank.send_to_database(self.sql_connector, sql, values)

            self.update()
            return True

        def _create_chech_list(self):

            l = []

            for i in self.liste:
                sql = f"select * from regelwerk where TeilA = {i[0]}"

                result = datenbank.select_from_database(self.sql_connector, sql)

                if result[0] is not None:
                    for r in result:
                        l += [r.get("TeilB")]

                sql = f"select * from regelwerk where TeilB = {i[0]}"

                result = datenbank.select_from_database(self.sql_connector, sql)

                if result[0] is not None:
                    for r in result:
                        l += [r.get("TeilA")]

            self.check_list = l

        def add_to_other(self, id, konf):
            if konf:
                sql = f"""insert into  konfigurationenpos(KonfigurationID, Position, ProduktID) values(?,?,?)"""

                for i in self.liste:
                    values = (int(id), i[0], i[1])
                    datenbank.send_to_database(self.sql_connector, sql, values)
            else:
                sql = """insert into bestellungpos(BestellungID, Position, ProduktID, Menge, Preis, Summe) values(?,?,?,?,?,?)"""

                for i in self.liste:
                    values = (int(id), i[0], i[1], i[2], i[3], i[4])
                    datenbank.send_to_database(self.sql_connector, sql, values)

    class Konfigurationpositionen(Bestellpositionen):
        def _get_artike(self, index):

            return self.artikel_list[index]

        def create_positionen_list(self):

            pos_list = []

            sql = f"""select Position,KonfigurationID,konfigurationenpos.ProduktID,Bezeichnung,Preis 
            from Konfigurationenpos left join produkte p on p.ProduktID = konfigurationenpos.ProduktID 
            where KonfigurationID = {self.id}"""

            results = datenbank.select_from_database(self.sql_connector, sql)

            if results[0] is not None:
                for eintrag in results:
                    pos_list += [
                        [
                            eintrag.get("Position"),
                            int(eintrag.get("ProduktID")),
                            0,
                            eintrag.get("Preis"),
                            0,
                            eintrag.get("Bezeichnung"),
                        ]
                    ]

            self.liste = pos_list

        def create_label_list(self):

            self.label_list = []

            for row in self.liste:
                self.label_list += [f"{row[0]}|{row[5]}"]

        def sum(self):

            self.summeN = 0
            self.summeB = 0

        def delete(self, index):

            artikel = self.liste[index]

            slq = f"delete from konfigurationenpos where Position = ? and KonfigurationID = ? "
            values = (artikel[0], self.id)

            datenbank.send_to_database(self.sql_connector, slq, values)

            self.update()

        def add(self, index, preis, menge):

            sql = "insert into konfigurationenpos(KonfigurationID, Position,ProduktID) values(?,?,?)"

            artikel = self._get_artike(index)

            if artikel[0] in self.check_list:
                return False

            values = (self.id, self.get_new_id(), artikel[0])

            datenbank.send_to_database(self.sql_connector, sql, values)

            self.update()
            return True

        def save(self, index, preis, menge, index2):
            sql = f"""UPDATE konfigurationenpos 
                        set 

                        ProduktID = ?
    
                        where

                        KonfigurationID = ?

                        and

                        Position = ?
                         """

            artikel = self._get_artike(index)

            if artikel[0] in self.check_list:
                return False

            values = (artikel[0], self.id, self.liste[index2][0])

            datenbank.send_to_database(self.sql_connector, sql, values)

            self.update()
            return True


class Konflikte:

    # TODO

    def __init__(self, produkt_id, konflikte, konflikte_name):
        self.produkt_id = produkt_id
        self.konflikte_liste = konflikte
        self.konflikte_name = konflikte_name


class Kunde:
    def __init__(
        self,
        id=None,
        nachname=None,
        name=None,
        geburtsdatum=None,
        e_mail=None,
        plz=None,
        ort=None,
        strasse=None,
        hausnummer=None,
        heandler=None,
        firma=None,
    ):

        self.firma = firma
        self.heandler = heandler
        self.hausnummer = hausnummer
        self.strasse = strasse
        self.ort = ort
        self.plz = plz
        self.e_mail = e_mail
        if geburtsdatum is not None:
            self.geburtsdatum = datetime.datetime(
                year=int(geburtsdatum[0:4]),
                month=int(geburtsdatum[5:7]),
                day=int(geburtsdatum[8:10]),
            )
        else:
            self.geburtsdatum = datetime.datetime(year=1900, month=1, day=1)
        self.name = name
        self.nachname = nachname
        # if muss in jeder Klasse den Primärschlüssel aus der Datenbank beinhalten
        self.id = id
        # Label definiert, wie die Einträge in der Suchliste angezeigt werden
        self.label = None
        self.hilfs_eintrag = None
        # Hilfseintrag erweitert die Suche um spezielle Funktionen zu erweitern
        # In diesem Fall kann man über die Eingabe "Händler" alle Händler anzeigen.
        if self.heandler == 0:
            self.label = f"{self.id} | {self.name} {self.nachname}"
            self.hilfs_eintrag = "kein Händler"

        else:
            self.label = f"{self.id} | {self.firma}"
            self.hilfs_eintrag = "Händler"

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __str__(self):

        ausgabe = "--------------------------------------------------\n"

        for i in vars(self):
            ausgabe += str(i) + "    " + str(vars(self)[i]) + "\n"

        ausgabe += "----------------------------------------------------"
        return ausgabe


class ObjectListe:
    def __init__(self):
        self.liste = []
        self.index = 0

        self.sql_connector = datenbank.create_connection()
        self.fehlermeldung = ""
        self._searchliste = self._create_search_list()
        self.suchgenauigkeit = 4

    def search(self, search_string):
        """
        Implementiert eine Methode, in welcher mit hilfe von einem Keywords nach Treffer gesucht werden kann.
        Die Treffer werden dann in die Objectliste eingefügt.
        Die Funktion gibt einen Liste mit [gefundenem Eintrag, String-Unterschied zurück]. Die liste ist aufsteigend
        Sortiert. Kommunikation mit der Datenbank wird in den Subclassen implementiert.

        :param search_string: Suchstring
        :return: List[id_treffer, Unterschied]
        """
        self.liste = []
        id_list = []

        if search_string == "":
            for eintrag in self._searchliste:
                id_list += [[int(eintrag[1]), 0]]

            return id_list

        for eintrag in self._searchliste:

            min_distance = 1000

            for strings in eintrag[1:]:

                distance = get_levenshtein_distanz(search_string, strings)

                if distance < min_distance:
                    min_distance = distance

            if min_distance < self.suchgenauigkeit:
                id_list += [[int(eintrag[1]), min_distance]]

        return sorted(id_list, key=lambda l: l[1], reverse=False)

    def get_label_list(self):
        """
        Diese Funktion erstellt eine Liste allen labels der in ObjectList gespeicherten Einträgen
        :return:
        """

        label_list = []

        for i in self.liste:
            label_list += [i.label]

        return label_list

    def set_current(self, index):
        """
        Methode ermöglicht das aktuelle Object zu definieren
        :param index: int
        :return:
        """
        self.index = index

    def get_current(self):
        """
        Gibt das aktuelles Object aus der Liste zurück

        :return: aktuelles Object oder None wenn Liste leer ist
        """
        if self.liste:

            return self.liste[self.index]
        else:
            return None

    def __str__(self):
        result = ""
        if self.liste:
            for eintrag in self.liste:
                result += str(eintrag) + "\n"
        else:
            result = "LEER"

        return result

    def _create_search_list(self, dic):
        """
        Methode erstellt eine searchlist für die Schlüsselwortsuche
        :param dic:
        :return:
        """

        liste = []
        try:
            for eintrag in dic:
                a = [next(iter(eintrag.values()))]
                for zeile in eintrag.values():
                    if zeile != None:
                        if isinstance(zeile, str):
                            a += zeile.split("|")
                        else:
                            a += [str(zeile).lower()]
                liste += [a]
        except:
            pass

        return liste

    def exist(self, id):
        """
        Methode gibt zurück ob element mit id existiert
        :param id:
        :return:
        """
        try:
            for eintrag in self._searchliste:
                if eintrag[0] == int(id):
                    return True

            return False
        except ValueError:
            return False

    def update(self):
        self._searchliste = self._create_search_list()


class KundenListe(ObjectListe):
    def search(self, search_string):
        """
        Methode fügt aus der Oberklassen-Funktion erstellten Trefferliste einträge in die Kundenliste ein.
        :param search_string:
        :return:
        """

        id_list = super().search(search_string)

        for eintrag in id_list:

            result_liste = datenbank.select_from_database(
                self.sql_connector,
                f"select * from kunden where KundenID = {eintrag[0]}",
            )

            for r in result_liste:
                self.liste.append(
                    Kunde(
                        r.get("KundenID"),
                        r.get("Nachname"),
                        r.get("Name"),
                        r.get("Geburtsdatum"),
                        r.get("EMail"),
                        r.get("PLZ"),
                        r.get("Ort"),
                        r.get("Strasse"),
                        r.get("Hausnummer"),
                        r.get("Haendler"),
                        r.get("Firma"),
                    )
                )

    def _create_search_list(self):
        """Funktion erstellt eine Searchlist für die Unterklasse"""

        search_dic = datenbank.select_from_database(
            self.sql_connector, "select * from kunden"
        )

        return super()._create_search_list(search_dic)

    def delete(self, id):
        """
        Methode realisiert die Möglichkeit, Einträge aus der Datenbank zu löschen
        :param id:
        :return:
        """

        result = datenbank.send_to_database(
            self.sql_connector,
            f"DELETE FROM kunden where KundenID = ?",
            (self.liste[id].id,),
        )
        self.update()

        if isinstance(result, str):

            log.error("Fehler aufgetreten: " + result)

        else:
            log.info("Eintrag erfolgreich gelöscht")

    def save(
        self,
        id,
        name,
        nachname,
        geburtsdatum,
        plz,
        ort,
        mail,
        strasse,
        hausnummer,
        heandler,
        firma,
    ):
        """
        Mode implementiert das Erstellen und Abändern von Einträgen in der Datenbank. Dazu wird am Anfang überprüft,
        ober der Eintrag schon Vorhanden ist, und entsprechen angeändert oder neu erstellt.
        :param id:
        :param name:
        :param nachname:
        :param geburtsdatum:
        :param plz:
        :param ort:
        :param mail:
        :param strasse:
        :param hausnummer:
        :param heandler:
        :param firma:
        :return:
        """

        if self.exist(id):
            sql_statement = f"""
            
            UPDATE kunden
            
            Set 
                Name = ?,
                Nachname = ?,
                Geburtsdatum = ?,
                EMail = ?,
                PLZ = ?,
                Ort = ?,
                Strasse = ?,
                Hausnummer = ?,
                Haendler = ?,
                Firma = ?,
                hilfe = ?
            WHERE 
                KundenID = ?
            """

            parameter = (
                None if name == "" else str(name),
                None if nachname == "" else str(nachname),
                None
                if geburtsdatum.year == 1900
                else f"{geburtsdatum.year}-{str(geburtsdatum.month).zfill(2)}-{str(geburtsdatum.day).zfill(2)}",
                None if mail == "" else str(mail),
                None if plz == "" else str(plz),
                None if ort == "" else str(ort),
                None if strasse == "" else str(strasse),
                None if hausnummer == "" else str(hausnummer),
                1 if heandler else 0,
                None if firma == "" else str(firma),
                "Händler" if heandler else None,
                id,
            )

            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, parameter
            )

            if isinstance(result, str):

                log.error("Fehler aufgetreten: " + result)

            else:
                log.info("Eintrag erfolgreich geändert")

        else:

            sql_statement = f"""
            
            INSERT INTO kunden VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                
                
            """
            values = (
                id,
                None if nachname == "" else str(nachname),
                None if name == "" else str(name),
                None
                if geburtsdatum.year == 1900
                else f"{geburtsdatum.year}-{str(geburtsdatum.month).zfill(2)}-{str(geburtsdatum.day).zfill(2)}",
                None if mail == "" else str(mail),
                None if plz == "" else str(plz),
                None if ort == "" else str(ort),
                None if strasse == "" else str(strasse),
                None if hausnummer == "" else str(hausnummer),
                1 if heandler else 0,
                None if firma == "" else str(firma),
                "Händler" if heandler else None,
            )
            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, values
            )

            if isinstance(result, str):

                log.error("Fehler aufgetreten: " + result)

            else:
                log.info("Eintrag erfolgreich Erstellt")

        self.update()


class BestellungListe(ObjectListe):

    # TODO
    def _create_search_list(self):

        search_dic = datenbank.select_from_database(
            self.sql_connector,
            """select BestellungID
        ,kunden.KundenID,Datum,Bestellsumme,
        Bezahlt, Bezahlt_am ,Nachname,Firma,bestellung.hilfe from bestellung left join kunden
         on bestellung.KundenID = kunden.KundenID""",
        )
        search_dic += datenbank.select_from_database(
            self.sql_connector,
            """select KonfigurationID, kunden.KundenID, konfigurationen.hilfe, Nachname,Firma
from konfigurationen left join kunden on konfigurationen.KundenID = kunden.KundenID""",
        )

        return super()._create_search_list(search_dic)

    # TODO
    def search(self, search_string, customerID=None, konfi=False):

        self.suchgenauigkeit = 2

        self.liste = []
        id_list = []

        if search_string == "":
            for eintrag in self._searchliste:
                if "Konfiguration" in eintrag:
                    id_list += [[int(eintrag[1]), 0, 0]]
                else:
                    id_list += [[int(eintrag[1]), 0, 1]]

        else:
            for eintrag in self._searchliste:

                min_distance = 1

                for strings in eintrag[1:]:

                    distance = get_levenshtein_distanz(search_string, strings)

                    if distance < min_distance:
                        min_distance = distance

                if min_distance < self.suchgenauigkeit:
                    if "Konfiguration" in eintrag:
                        id_list += [[int(eintrag[1]), min_distance, 0]]
                    else:
                        id_list += [[int(eintrag[1]), min_distance, 1]]

        id_list = sorted(id_list, key=lambda l: (-l[2], l[1]), reverse=False)

        for eintrag in id_list:

            if eintrag[2] == 1:

                result_liste = datenbank.select_from_database(
                    self.sql_connector,
                    f"""select BestellungID
                                        ,kunden.KundenID,Datum,Bestellsumme,
                                        Bezahlt, Bezahlt_am ,Nachname,Firma from bestellung left join kunden
                                        on bestellung.KundenID = kunden.KundenID where BestellungID = {eintrag[0]}""",
                )

                for r in result_liste:
                    self.liste.append(
                        Bestellungen(
                            r.get("BestellungID"),
                            r.get("KundenID"),
                            r.get("Datum"),
                            r.get("Bestellsumme"),
                            r.get("Bezahlt"),
                            r.get("Bezahlt_am"),
                            False,
                            r.get("Firma"),
                            r.get("Nachname"),
                        )
                    )
            else:
                result_liste = datenbank.select_from_database(
                    self.sql_connector,
                    f"""select KonfigurationID, kunden.KundenID,konfigurationen.kundenID
                                                               hilfe, Nachname,Firma
                                                            from konfigurationen left join kunden on 
                                                            konfigurationen.KundenID = kunden.KundenID 
                                                            where KonfigurationID = {eintrag[0]}""",
                )

                for r in result_liste:
                    self.liste.append(
                        Bestellungen(
                            r.get("KonfigurationID"),
                            r.get("KundenID"),
                            None,
                            None,
                            None,
                            None,
                            True,
                            r.get("Firma", r.get("Nachname")),
                        )
                    )

        if customerID:
            newlist = []
            for order in self.liste:
                if (
                    str(order.kunden_id) == str(customerID)
                    and order.konfiguration == konfi
                ):
                    newlist.append(order)
            self.liste = newlist

    def save(
        self,
        session,
        id=None,
        kunden_id=None,
        datum=None,
        bestellsumme=None,
        bezahlt=None,
        bezahldatum=None,
        konfiguration=False,
    ):

        if not session.kunden.exist(kunden_id):
            return False

        if konfiguration:
            self.save_konfiguration(id, kunden_id)

        else:
            self.save_bestellung(
                id, kunden_id, datum, bestellsumme, bezahlt, bezahldatum
            )

        self.update()

        return True

    def save_konfiguration(self, id, kunden_id):

        if self.exist(id, True):
            sql_statement = f"""

            UPDATE konfigurationen

            Set 
                KundenID = ?
            WHERE 
                KonfigurationID = ?
            """

            parameter = (kunden_id, id)

            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, parameter
            )

            if isinstance(result, str):

                print("Fehler aufgetreten: " + result)

            else:
                print("Eintrag erfolgreich geändert")

        else:

            sql_statement = f"""

            INSERT INTO konfigurationen(KonfigurationID,KundenID) VALUES(?,?)


            """
            values = (id, kunden_id)
            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, values
            )

            if isinstance(result, str):

                print("Fehler aufgetreten Konfiguration: " + result)

            else:
                print("Eintrag erfolgreich Erstellt")

        self.update()

    def save_bestellung(
        self,
        id=None,
        kunden_id=None,
        datum=None,
        bestellsumme=None,
        bezahlt=False,
        bezahldatum=None,
    ):
        if self.exist(id, False):
            sql_statement = f"""

            UPDATE bestellung

            Set 
                KundenID = ?,
                Datum = ?,
                Bestellsumme = ?,
                Bezahlt = ?,
                Bezahlt_am = ?,
                hilfe = ?
            WHERE 
                BestellungID = ?
            """

            parameter = (
                int(kunden_id),
                None
                if datum.year == 1900
                else f"{datum.year}-{str(datum.month).zfill(2)}-{str(datum.day).zfill(2)}",
                None if bestellsumme == "" else float(bestellsumme),
                1 if bezahlt else 0,
                None
                if bezahldatum.year == 1900
                else f"{bezahldatum.year}-{str(bezahldatum.month).zfill(2)}-{str(bezahldatum.day).zfill(2)}",
                "Bezahlt" if bezahlt else None,
                int(id),
            )

            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, parameter
            )

            if isinstance(result, str):

                print("Fehler aufgetreten Bestellung insert:  " + result)

            else:
                print("Eintraf erfolgreich geändert")

        else:

            sql_statement = f"""

            INSERT INTO bestellung VALUES(?,?,?,?,?,?,?)


            """
            values = (
                int(id),
                int(kunden_id),
                None
                if datum.year == 1900
                else f"{datum.year}-{str(datum.month).zfill(2)}-{str(datum.day).zfill(2)}",
                None if bestellsumme == "" else float(bestellsumme),
                1 if bezahlt else 0,
                None
                if bezahldatum.year == 1900
                else f"{bezahldatum.year}-{str(bezahldatum.month).zfill(2)}-{str(bezahldatum.day).zfill(2)}",
                "Bezahlt" if bezahlt else None,
            )
            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, values
            )

            if isinstance(result, str):

                print("Fehler aufgetreten Bestellung: " + result)

            else:
                print("Eintrag erfolgreich Erstellt")

        self.update()

    def delete(self, id, konfiguration):

        a = "konfigurationen" if konfiguration else "bestellung"
        b = "KonfigurationID" if konfiguration else "BestellungID"
        result = datenbank.send_to_database(
            self.sql_connector, f"delete from {a} where {b} = ?", (int(id),)
        )

        if isinstance(result, str):

            print("Fehler aufgetreten: " + result)

        else:
            print("Eintrag erfolgreich gelöscht")

        self.update()

    def exist(self, id, konfiguration):
        """
        Methode gibt zurück ob element mit id existiert
        :param id:
        :return:
        """
        if konfiguration:
            for eintrag in self._searchliste:
                if eintrag[0] == int(id) and "Konfiguration" in eintrag:
                    return True
        else:
            for eintrag in self._searchliste:
                if eintrag[0] == int(id):
                    return True
        return False

    def update(self):
        self._searchliste = self._create_search_list()


class ArtikelListe(ObjectListe):
    def __init__(self):
        super().__init__()
        self.produktkategorie = self._create_produkt_kategorien()

    def get_label_list(self):

        label_list = []

        for i in self.liste:
            label_list += [[i.label, i.nachbestellen]]

        return label_list

    def update(self):

        self.produktkategorie = self._create_produkt_kategorien()
        super().update()

    # TODO
    def _create_search_list(self):
        search_dic = datenbank.select_from_database(
            self.sql_connector,
            """select ProduktID,produkte.Bezeichnung,Produktkategorie
         ,Preis,Lagerfach,Bestand,Meldebestand,Produkt_Bezeichnung,hilfe  from produkte
         left join produktkategorie where produkte.Produktkategorie = produktkategorie.KategorieID""",
        )

        return super()._create_search_list(search_dic)

    def _create_produkt_kategorien(self):

        search_dic = datenbank.select_from_database(
            self.sql_connector, "SELECT * FROM produktkategorie"
        )

        return super()._create_search_list(search_dic)

    # TODO
    def search(self, search_string):
        id_list = super().search(search_string)

        for eintrag in id_list:

            result_liste = datenbank.select_from_database(
                self.sql_connector,
                f"""select ProduktID,produkte.Bezeichnung,Produktkategorie
         ,Preis,Lagerfach,Bestand,Meldebestand,Produkt_Bezeichnung from produkte left join produktkategorie 
                                                          on produkte.Produktkategorie = produktkategorie.KategorieID
                                                           where ProduktID = {eintrag[0]}""",
            )

            for r in result_liste:
                self.liste.append(
                    Artikel(
                        r.get("ProduktID"),
                        r.get("Bezeichnung"),
                        r.get("Produktkategorie"),
                        r.get("Produkt_Bezeichnung"),
                        r.get("Preis"),
                        r.get("Lagerfach"),
                        r.get("Bestand"),
                        r.get("Meldebestand"),
                    )
                )

    def delete(self, id):
        result = datenbank.send_to_database(
            self.sql_connector,
            f"DELETE FROM produkte where ProduktID = ?",
            (self.liste[id].id,),
        )
        self.update()

        if isinstance(result, str):

            print("Fehler aufgetreten: " + result)

        else:
            print("Eintraf erfolgreich gelöscht")

    # TODO
    def save(
        self,
        id,
        bezeichnung,
        produktkatgorie_ID,
        preis,
        lagerfach,
        bestand,
        meldebestand,
    ):
        if self.exist(id):
            sql_statement = f"""

                   UPDATE produkte

                   Set 
                       
                       Bezeichnung = ?,
                       Produktkategorie = ?,
                       Preis = ?,
                       Lagerfach = ?,
                       Bestand = ?,
                       Meldebestand = ?,
                       hilfe = ?
                     
                   WHERE 
                       ProduktID = ?
                   """

            parameter = (
                None if bezeichnung == "" else str(bezeichnung),
                None if produktkatgorie_ID == "" else int(produktkatgorie_ID),
                None if preis == "" else float(preis),
                None if lagerfach == "" else str(lagerfach),
                None if bestand == "" else int(bestand),
                None if meldebestand == "" else int(meldebestand),
                "Nachbestellen" if int(bestand) <= int(meldebestand) else None,
                int(id),
            )

            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, parameter
            )

            if isinstance(result, str):

                print("Fehler aufgetreten: " + result)

            else:
                print("Eintraf erfolgreich geändert")

        else:

            sql_statement = f"""

                   INSERT INTO produkte VALUES(?,?,?,?,?,?,?,?)


                   """
            values = (
                int(id),
                None if bezeichnung == "" else str(bezeichnung),
                None if produktkatgorie_ID == "" else int(produktkatgorie_ID),
                None if preis == "" else float(preis),
                None if lagerfach == "" else str(lagerfach),
                0 if type(bestand) == str else int(bestand),
                0 if type(meldebestand) == str else int(meldebestand),
                "Nachbestellen"
                if type(bestand) == str
                and type(meldebestand) == str
                and int(bestand) <= int(meldebestand)
                else None,
            )
            result = datenbank.send_to_database(
                self.sql_connector, sql_statement, values
            )

            if isinstance(result, str):

                print("Fehler aufgetreten: " + result)

            else:
                print("Eintrag erfolgreich Erstellt")

        self.update()


class KonfliktListe(ObjectListe):
    def __init__(self):
        super().__init__()
        self.artikel_liste = self._create_artikel_list()
        self.index = -1
        self.search()

    # TODO

    def get_konflikte(self, id):
        for i in self.liste:
            if i.produkt_id == int(id):
                return i.konflikte_name

        return []

    def get_index_id(self, id):
        for i in range(len(self.liste)):
            if self.liste[i].produkt_id == int(id):
                return i

        return -1

    def _create_search_list(self):

        return

    def _create_artikel_list(self):

        liste = []

        sql = f"select ProduktID,Bezeichnung from produkte"

        result = datenbank.select_from_database(self.sql_connector, sql)

        for r in result:
            liste += [[r.get("ProduktID"), r.get("Bezeichnung")]]

        return liste

    def update(self):

        self.artikel_liste = self._create_artikel_list()
        super().update()

    # TODO
    def search(self):
        self.artikel_liste = self._create_artikel_list()
        self.liste = []

        neue_liste = []

        sql = "select ProduktID from produkte"

        result = datenbank.select_from_database(self.sql_connector, sql)

        for r in result:

            konflikte = []
            konflikte_name = []

            k1 = datenbank.select_from_database(
                self.sql_connector,
                f"select TeilB from regelwerk where TeilA = {r.get('ProduktID')}",
            )

            if k1[0] is not None:
                for k in k1:
                    name = datenbank.select_from_database(
                        self.sql_connector,
                        f"select Bezeichnung from  produkte where ProduktID = {k.get('TeilB')}",
                    )
                    konflikte += [k.get("TeilB")]
                    konflikte_name += [name[0].get("Bezeichnung")]
            k2 = datenbank.select_from_database(
                self.sql_connector,
                f"select TeilA from regelwerk where TeilB = {r.get('ProduktID')}",
            )

            if k2[0] is not None:
                for k in k2:
                    name = datenbank.select_from_database(
                        self.sql_connector,
                        f"select Bezeichnung from  produkte where ProduktID = {k.get('TeilA')}",
                    )

                    if name[0] is not None:
                        konflikte += [k.get("TeilA")]
                        konflikte_name += [name[0].get("Bezeichnung")]

            self.liste += [Konflikte(r.get("ProduktID"), konflikte, konflikte_name)]

    # TODO
    def delete(self, id):

        a = datenbank.send_to_database(
            self.sql_connector,
            f"delete from regelwerk where TeilA = ? and TeilB = ?",
            (self.get_current().produkt_id, self.get_current().konflikte_liste[id]),
        )

        self.search()

    # TODO
    def save(self, id):

        if self.artikel_liste[id][0] in self.get_current().konflikte_liste:
            return False

        a = datenbank.send_to_database(
            self.sql_connector,
            f"insert into regelwerk values(?,?)",
            (self.get_current().produkt_id, self.artikel_liste[id][0]),
        )

        self.search()
        return True


def test():
    test_liste = KundenListe()

    test_user = User()

    test_liste.search("1970")

    log.debug(test_liste._searchliste)

    log.debug(test_liste)


if __name__ == "__main__":
    test()
