from datetime import date
import sys

sys.path.insert(2, "..\\libs")
from libs.log import Logger

log = Logger("syslog", "datev")


class Buchung:
    def __init__(self, konto, betrag, buchungsdatum, bemerkung):
        self.konto = str(konto)
        self.betrag = str(betrag)
        self.buchungsdatum = str(buchungsdatum)
        self.bemerkung = str(bemerkung)
        self.bunchungstext = (
            "{konto} \t {betrag} \t {buchungsdatum} \t {bemerkung}".format(
                konto=self.konto,
                betrag=self.betrag,
                buchungsdatum=self.buchungsdatum,
                bemerkung=self.bemerkung,
            )
        )


class Buchunsstapel:
    def __init__(self):
        self.stapel = []

    def add_buchung(self, betrag, buchungsdatum, bemerkung, konto="4200"):
        buchung = Buchung(konto, betrag, buchungsdatum, bemerkung)
        self.stapel.append(buchung)
        log.info("Buchung zu Buchunsstapel hinzugefügt")

    def clear(self):
        self.stapel = []
        log.info("Buchunsstapel restet")


class DatevExporter:
    def __init__(self, absender, kodierung, speicherort="DatevExport"):
        self.absender = str(absender)
        if kodierung != "UTF-8" and kodierung != "ASCII":
            raise Exception(
                "Kodierung muss UTF-8 oder ASCII sein. Nicht: " + str(kodierung)
            )
        self.kodierung = kodierung
        self.output = ""
        self.buchungsstapel = Buchunsstapel()
        self.speicherort = speicherort
        log.info("neuer DatevExporter initiert")

    def get_header(self, datum):
        header = "Absender: " + self.absender
        header += "\nExport: " + datum
        header += "\nKodierung: " + self.kodierung
        header += "\nKonto \t Betrag \t Buchungsdatum \t Bemerkung"
        return header

    def create_file(self, name, inhalt):
        try:
            rechnungsdatei = open(self.speicherort + "/" + name + ".txt", "w+")
        except:
            log.error(
                "Dateipfad existiert nicht: " + self.speicherort + "/" + name + ".txt"
            )
            raise Exception("Dateipfadfehler")
        rechnungsdatei.write(inhalt)
        rechnungsdatei.close()
        log.info("Datevfile: " + name + " wurde erstellt")

    def export(self, filename):
        datum = str(date.today())
        self.output += self.get_header(datum)
        for buchung in self.buchungsstapel.stapel:
            self.output += "\n" + buchung.bunchungstext
        self.create_file(str(filename), self.output)
        self.output = ""
        log.info("Datevexport abgeschlossen")
        return True
