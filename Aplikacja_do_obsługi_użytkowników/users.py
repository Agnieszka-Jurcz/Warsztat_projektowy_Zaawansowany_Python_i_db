import argparse
from xxlimited_35 import error

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
    else:

        except UniqueViolation as e:
        print ("User already exists", e)

def list(cursor, list):
    user = User.load_all_users(cursor)
    for user in user:
        print (user.username)

if __name__ == '__main__':
    try:
pass

#cdn....





