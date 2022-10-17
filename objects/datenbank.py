import sqlite3


def create_connection():
    """
    Erstellt eine Verbindung zur Datenbank.
    :return: SQL Connection Object. None bei Fehler

    """
    connection = None
    try:
        connection = sqlite3.connect("objects/Datenbank.db",timeout=1)
        connection.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(e)
    return connection


def select_from_database(connection, sql_statement):
    """
    Methode gibt Liste mit den Ergebnissen der übergebenen Query zurück. Sollte ein Sql_Fehler
    auftreten so wir [None, "Fehlermeldung] Zurückgegeben

    :param sql_statement:
    :param connection: Sqlite connection Object
    :param sql: Sql-Befehl
    :return: list mit dictionary der Ergebnisse
    """
    result = []

    if connection == None:

        connection = create_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            sql_statement,
        )

        result = [dict(row) for row in cursor.fetchall()]
        cursor.close()

        if not result:
            result = [None, "Kein Treffer in der Datenbank"]
    except sqlite3.Error as e:
        result = [None, e]

    return result


def send_to_database(connection, query_statement, values):
    """
    Implementiert die Funktion, mit der Datenbank zu kommunizieren. Über Values können parameter übergeben werden.


    :param connection:
    :param query_statement:
    :param values:
    :return: True wenn erfolgreich, String mit Fehlermeldung anderenfalls.
    """
    result = True
    try:
        cursor = connection.cursor()
        cursor.execute(query_statement, values)
        connection.commit()

    except sqlite3.Error as e:

        result = str(e)
    return result


def test():
    """
    Test Funktion

    """

    test_conn = create_connection()

    a = select_from_database(test_conn, "select * from verifikation")

    if a[0] is None:
        print(a[1])
        return

    for i in a:
        print(i)


if __name__ == "__main__":
    test()
