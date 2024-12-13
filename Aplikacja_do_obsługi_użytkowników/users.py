import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from clcrypto import check_password
from models import User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new_pass (min 8 characters)")
parser.add_argument("-l", "--list", help="list", action="store_true")
parser.add_argument("-d", "--delete", help="delete", action="store_true")
parser.add_argument("-e", "--edit", help="edit", action="store_true")

args = parser.parse_args()

def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)

    if not user:
        print ("User not exist")

    elif check_password(password, user.hashed_password):

        if len(new_pass)<8:
            print ("Password is too short. Please choose less than 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print ("Password changed successfully")
    else:
        print ("Incorrect password")

def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)

    if not user:
        print ("User not exist")
    elif check_password(password, user.hashed_password):
        user.delete_from_db(cursor)
        print ("User deleted successfully")
    else:
        print ("Incorrect password")

def new_user(cursor, username, password):
    if len(password)<8:
        print ("Password is too short. Please choose less than 8 characters.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print("User created successfully")
        except UniqueViolation as e:
            print ("User already exists", e)

def list(cursor):
    user = User.load_all_users(cursor)
    for user in user:
        print (user.username)

if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")  # Tutaj otwierane jest połączenie z bazą danych. Funkcja connect() pochodzi prawdopodobnie z biblioteki, takiej jak psycopg2, która służy do łączenia się z bazą danych PostgreSQL. Parametry wskazują nazwę bazy danych (workshop), nazwę użytkownika (postgres), hasło (coderslab) oraz hosta (127.0.0.1 oznacza lokalny komputer).
        cnx.autocommit = True  # Ta linia ustawia tryb autocommit na True, co oznacza, że każda operacja na bazie danych (np. INSERT, UPDATE, DELETE) będzie natychmiast zapisywana w bazie, bez potrzeby ręcznego zatwierdzania transakcji (np. przez commit()).
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:  # Ten warunek sprawdza, czy zostały przekazane wszystkie wymagane argumenty: username, password, edit i new_pass. Jeśli tak, wywołana zostanie funkcja edit_user(), która umożliwia edytowanie użytkownika.
            edit_user(cursor, args.username, args.password, args.new_pass) #  Ta linia wywołuje funkcję edit_user(), która prawdopodobnie służy do edytowania danych użytkownika w bazie. Argumenty przekazywane to: kursor bazy danych (cursor), nazwa użytkownika (args.username), jego hasło (args.password), oraz nowe hasło (args.new_pass).
        elif args.username and args.password and args.delete: # Jeśli nie spełniony był poprzedni warunek, ale zostały przekazane argumenty username, password oraz delete, to warunek będzie prawdziwy i wywoła się funkcja usuwająca użytkownika.
            delete_user(cursor, args.username, args.password)   # Wywołanie funkcji delete_user(), która prawdopodobnie usuwa użytkownika z bazy danych na podstawie podanych argumentów: nazwa użytkownika (args.username) i hasło (args.password).
        elif args.username and args.password:   # Jeśli spełnione są tylko argumenty username i password (czyli nie ma żadnych dodatkowych operacji jak edytowanie czy usuwanie), przejdzie do tworzenia nowego użytkownika.
            create_user(cursor, args.username, args.password)  # Wywołanie funkcji create_user(), która tworzy nowego użytkownika w bazie danych, przekazując mu nazwę użytkownika (args.username) oraz hasło (args.password).
        elif args.list: #  Jeśli przekazany argument to list (czyli użytkownik chce wyświetlić listę użytkowników), warunek zostaje spełniony.
            list_users(cursor)  # Wywołanie funkcji list_users(), która prawdopodobnie wyświetla listę wszystkich użytkowników zapisanych w bazie danych.
        else:
            parser.print_help()  # Ta linia wywołuje metodę print_help() obiektu parser, która prawdopodobnie jest instancją klasy odpowiedzialnej za parsowanie argumentów wiersza poleceń (np. z biblioteki argparse). Dzięki temu użytkownik otrzyma pomoc dotyczącą dostępnych opcji uruchomienia skryptu.
        cnx.close()
    except OperationalError as err:  # Ten blok except łapie wyjątek OperationalError, który może wystąpić, jeśli wystąpi problem z połączeniem do bazy danych lub wykonaniem operacji.
        print("Connection Error: ", err)








