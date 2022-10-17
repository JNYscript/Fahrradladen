# Zweirad’s Fahrradladen

## 1.Beschreibung

Zweirad’s Fahrradladen ist eine Software, die es dem Nutzer ermöglicht
Kundendaten, Artikeldaten und Bestellungen einzugeben, zu suchen und zu
verwalten. Außerdem besteht die Möglichkeit nicht kompatible Produkte
einzugeben.

## 2.Installation

**Python:**

1. "pip install requirements.txt" ist zum Installieren der Python Module.
2. Programm kann über "python setup.py" gestartet werden.



## 3. Login


Eingabe dieser Kombination ermöglicht den Zugriff auf das Programm. 

Aktuell existieren folgende Benutzer:

Benutzer: Zweirad; Kennwort: Dreirad

Benutzer: Mitarbeiter; Kennwort: Einrad

## 4.  Anleitung

#### 4.1 Suchfunktionen

Man kann entweder nach Eigenschaften der Objekte oder nach speziellen
Kriterien, die in den Unterpunkten angegeben sind, suchen.

#### 4.2 config.ini
in config.ini können Parameter wie die DATEV support Adresse geändert werden.

#### 4.3 Shortcuts
Das Programm verfügt über Shortcuts, welche beim darüber hovern über Elemente angezeigt werden. 

#### 4.4 Kunden

Um Kundendaten zu suchen, muss das gesuchte Merkmal in die Suchleiste im
oberen Teil des Fensters eingegeben werden. Mit einem Klick auf „Los“
oder der Betätigung der Enter-Taste werden ähnliche Einträge ausgegeben.
Der Eintrag mit der höchsten Übereinstimmung wird ganz oben angezeigt.
Um Kunden hinzuzufügen sind rechts im Fenster die jeweiligen Kundendaten
einzugeben und die Eingaben mit dem Button „Neuer Kunde“ zu bestätigen.
Es ist möglich durch einen Klick in das Feld „ist Händler“ den Kunden
als Firma mit dem Firmennamen zu registrieren. Kunden können gelöscht
werden bzw. die Einträge geleert werden.

Schlagwörter für die Suche:"Händler", zeigt in der Suche alle Kunden mit
dem Eintrag "Händler" oben in der Liste an.

#### 4.4 Bestellungen

Um Bestelldaten zu suchen, muss das gesuchte Merkmal in die Suchleiste
im oberen Teil des Fensters eingegeben werden. Mit einem Klick auf „Los“
oder der Betätigung der Enter-Taste werden ähnliche Einträge ausgegeben.
Der Eintrag mit der höchsten Übereinstimmung wird ganz oben angezeigt.
Um neue Bestellungen hinzuzufügen sind rechts im Fenster die jeweiligen
Bestelldaten einzugeben die Eingaben müssen mit „Neue Bestellung“
bestätigt werden. Es kann ausgewählt werden, ob es sich um eine
Konfiguration handelt oder ob die Rechnung schon bezahlt ist. Dafür ist
eine Datumsangabe erforderlich. Bestellungen können gelöscht werden bzw.
die Einträge geleert werden. Bestellpositionen können über das "+" unten
links in der Positionsliste

Schlagwörter für die Suche:"Bezahlt", zeigt alle bezahlten Rechnungen
an. 

#### 4.5 Artikel

Um Artikeldaten zu suchen, muss das gesuchte Merkmal in die Suchleiste
im oberen Teil des Fensters eingegeben werden. Mit einem Klick auf „Los“
oder der Betätigung der Enter-Taste werden ähnliche Einträge ausgegeben.
Der Eintrag mit der höchsten Übereinstimmung wird ganz oben angezeigt.
Artikel können unter Eingabe der Artikelnummer und Bezeichnung
registriert und anschließend kategorisiert werden. Außerdem kann
Lagerfach, Bestand, Meldebestand und der Nettopreis angezeigt werden.
Dabei entstehende Konflikte werden ebenfalls angezeigt. Artikel können
gelöscht und Einträge geleert werden. Über den "+"-Button können neue
Kategorien erstellt werden. Rot markierte Eintäge zeigen an, dass der
Bestand kleiner oder gleich groß wie der Meldebestand ist.

Schlagwörter für die Suche:"Nachbestellen", zeigt alle Artikel an, bei
denen der Bestand kleiner oder gleich groß wie der Meldebestand ist.

#### 4.6 Regelwerk

Im Dropdownmenü kann nach einem Artikel gesucht werden, für den die
Inkompatiblen Artikel in einer Liste ausgegeben werden. Oben kann in
einem Dropdownmenü ein Artikel ausgewählt werden und im rechten
Dropdownmenü ein inkompatibler Artikel ausgesucht werden. Die Eingabe
muss mit „Neuer Konflikt“ bestätigt werden. Außerdem können bestehende
Konflikte gelöscht werden.

## 5. Logout

Durch Betätigung der Logout Taste kann sich der Benutzer abmelden.

## 6. Änderungen in der Datenbank

Es wurde eine Verifizierungstabelle eingefügt mit den Spalten:
Benutzername, Passwort-Hash, Salt Einige schon bestehende Tabellen
wurden um die Spalte "Hilfe" erweitert, in dieser Spalte können
Schlagwörter eingegeben werden, mit denen nach Objekten gesucht werden
kann.



