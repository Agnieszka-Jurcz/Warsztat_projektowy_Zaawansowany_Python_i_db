from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable


CREATE_DB = "CREATE DATABASE workshop;"

CREATE_USERS_TABLE = """CREATE TABLE users(
    id serial PRIMARY KEY, 
    username varchar(255) UNIQUE,
    hashed_password varchar(80))"""

CREATE_MESSAGES_TABLE = """CREATE TABLE messages(
    id SERIAL, 
    from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
    text varchar(255),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""

DB_USER = "postgres"
DB_PASSWORD = "coderslab"
DB_HOST = "127.0.0.1"

try:
    cnx = connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST) #Próbujemy połączyć się z serwerem PostgreSQL za pomocą danych konfiguracyjnych
    cnx.autocommit = True  #Włącza tryb automatycznego zatwierdzania transakcji, co oznacza, że zmiany w bazie danych są zapisywane natychmiast po ich wykonaniu, bez konieczności wywoływania commit().
    cursor = cnx.cursor()  # tworzy obiekt kursora, który jest używany do wykonywania zapytań SQL na bazie danych.
    try:
        cursor.execute(CREATE_DB)  # Wykonuje zapytanie SQL, które jest zapisane w zmiennej CREATE_DB. To zapytanie powinno zawierać kod tworzenia nowej bazy danych.
        print("Database created")
    except DuplicateDatabase as e:
        print("Database exists ", e)
    cnx.close()   # Po wykonaniu zapytania zamykamy połączenie z serwerem PostgreSQL.
except OperationalError as e:  # Jeśli wystąpi błąd związany z połączeniem z bazą danych (np. brak dostępu, zły użytkownik lub hasło), zostanie przechwycony wyjątek
    print("Connection Error: ", e)

try:
    cnx = connect(database="workshop", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)  #  Łączymy się teraz z już istniejącą bazą danych workshop na tym samym serwerze PostgreSQL.
    cnx.autocommit = True  # Włączenie automatycznego zatwierdzania transakcji.
    cursor = cnx.cursor()   # tworzymy obiekt kursora do wykonywania zapytań na bazie workshop.

    try:
        cursor.execute(CREATE_USERS_TABLE)   # Wykonuje zapytanie SQL zapisane w zmiennej CREATE_USERS_TABLE, które tworzy tabelę users w bazie workshop.
        print("Table users created")  # Jeśli zapytanie zakończy się sukcesem, zostanie wyświetlony komunikat "Table users created".
    except DuplicateTable as e:
        print("Table exists ", e)

    try:
        cursor.execute(CREATE_MESSAGES_TABLE)  # Wykonuje zapytanie SQL zapisane w zmiennej CREATE_MESSAGES_TABLE, które tworzy tabelę messages.
        print("Table messages created")   # Po udanym wykonaniu zapytania wyświetli się komunikat "Table messages created".
    except DuplicateTable as e:
        print("Table exists ", e)
    cnx.close()
except OperationalError as e:
    print("Connection Error: ", e)

# Program łączy się z serwerem PostgreSQL, aby stworzyć nową bazę danych oraz dwie tabele w już istniejącej bazie workshop.
# Każde zapytanie (tworzenie bazy danych, tworzenie tabel) jest wykonane w bloku try, a błędy (np. jeśli baza danych lub tabela już istnieje) są obsługiwane w odpowiednich blokach except.
# W przypadku problemów z połączeniem do serwera, błąd jest przechwytywany i wyświetlany.