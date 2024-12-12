# Warsztat – Konfiguracja bazy danych

# 1. Stworzenie bazy danych create_db.py:

postgres=# CREATE DATABASE create_db;
CREATE DATABASE
postgres=# \c create_db

# 2. Stworzenie tabelę Users (id, username, hashed_password)

create_db=# CREATE TABLE Users (
create_db(# id SERIAL PRIMARY KEY,
create_db(# username VARCHAR(255) UNIQUE,
create_db(# hashed_password VARCHAR(80)
create_db(# );

# 3. Stworzenie tabelę Messages (id, from_id, to_id, creation_date, text)

create_db=# CREATE TABLE Messages (
create_db(# id SERIAL PRIMARY KEY,
create_db(# from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
create_db(# to_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
create_db(# creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
create_db(# text varchar(255)
create_db(# );