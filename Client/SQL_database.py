# SOURCE FILE:    SQL_database.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      Access point to MYSQL database
#                 It provides functions include make connection with database, 
#                 create database, create table, execute query, insert new record, 
#                 update existing record, get existing record value, and delete record. 
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
import mysql.connector
from mysql.connector import Error
import pandas as pd
import re


db =  "safeHouse"
pw = "960727syh"
#Connecting to MySQL Server
#root
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# connect with db
def make_connection():
    connection = create_db_connection("localhost", "root", pw, db)
    return connection

# Creating a New Database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

# Connecting to MySQL Server and access to my db 
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

# used when insert/update/delete record
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# used when select a record and get wanted value.
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# CREATE a new table in MYSQL database
def create_tables(connection):
    create_file_table = """
    CREATE TABLE files (
        name VARCHAR(40) PRIMARY KEY,
        status TINYINT DEFAULT 0,
        level TINYINT DEFAULT 0,
        cryptography VARCHAR(15) DEFAULT 'Null',
        aesEncrypt VARCHAR(15) DEFAULT 'Null',
        xorEncrypt VARCHAR(15) DEFAULT 'Null',
        rsaEncrypt VARCHAR(15) DEFAULT 'Null',
        EncryptionOrder VARCHAR(50) DEFAULT 'Null'
        );
     """
    execute_query(connection, create_file_table)

# INSERT a new file record into db
def insert_file_db(connection,filename,level):
    my_queue = "INSERT INTO files(name, level) VALUES ('"+filename+"', "+str(level)+");"
    execute_query(connection, my_queue)

# SELECT, get a file's encryption order from db
def get_encrypt_order(connection, filename):
    my_queue = "SELECT EncryptionOrder FROM files where name = '" + filename+"';"
    order = read_query(connection, my_queue)
    result = order[0]
    encrypt_order =re.sub(r"\W+|_", " ", str(result))
    encrypt_order =encrypt_order[1:-1]
    return encrypt_order

# SELECT, get a file's encryption key. (get one each time.)
def get_encrypt_keys(connection, filename, decrypt_order):
    decrypt_order_list = decrypt_order.split(" ")
    keys = ""
    for item in decrypt_order_list:
        my_queue = "SELECT "+item+" FROM files where name = '" + filename+"';"
        order = read_query(connection, my_queue)
        result = order[0]
        key = re.sub(r'[^._a-zA-Z0-9 \n\.]', '', str(result))
        key = key.strip()
        keys += key + " "
    return keys.strip()

# SELECT, all files in particular level folder
# return two list, one contain all normal files, the other contains all encrypted files. 
def get_file_names(connection,level):
    unencrypted_files_list = []
    encrypted_files_list = []

    my_queue = "SELECT name FROM files where status = 0 AND level = "+str(level)+";"
    unencrypted_files_sql = read_query(connection, my_queue)
    if len(unencrypted_files_sql) > 0:
        for item in unencrypted_files_sql:
            result = re.sub(r'[^._a-zA-Z0-9 \n\.]', '', str(item))
            unencrypted_files_list.append(result.strip())

    my_queue = "SELECT name FROM files where status = 1 AND level = "+str(level)+";"
    encrypted_files_sql = read_query(connection, my_queue)
    if len(encrypted_files_sql) > 0:
        for item in encrypted_files_sql:
            result = re.sub(r'[^._a-zA-Z0-9 \n\.]', '', str(item))
            encrypted_files_list.append(result.strip())
    return unencrypted_files_list, encrypted_files_list

# UPDATE, update the file record in db when it is encrypted. 
def encrypt_file_db(connection,filename, method, key):
    encrypt_order = get_encrypt_order(connection,filename)
    if encrypt_order == "Null":
        my_queue = "UPDATE files SET status = 1, "+method+" = '"+key+"' , EncryptionOrder = '"+method+"' where name = '"+filename+"';"
        execute_query(connection, my_queue)
    else:
        encrypt_order = method + " " + encrypt_order
        my_queue = "UPDATE files SET "+method+" = '"+key+"' , EncryptionOrder = '"+encrypt_order+"' where name = '"+filename+"';"
        execute_query(connection, my_queue)

# UPDATE, update the file record in db when it is decrypted. 
def decrypt_file_db(connection,filename, method):
    encrypt_order = get_encrypt_order(connection,filename)
    encrypt_order = encrypt_order.replace(method, '')
    if encrypt_order == "":
        encrypt_order = "Null"
    else:
        encrypt_order = encrypt_order[1:]

    if encrypt_order == "Null":
        my_queue = "UPDATE files SET status = 0, "+method+" = 'Null' , EncryptionOrder = '"+encrypt_order+"' where name = '"+filename+"';"
        execute_query(connection, my_queue)
    else:
        my_queue = "UPDATE files SET status = 1, "+method+" = 'Null' , EncryptionOrder = '"+encrypt_order+"' where name = '"+filename+"';"
        execute_query(connection, my_queue)

# DELETE, delete a record from db
def delete_file_db(connection,filename):
    my_queue = "DELETE from files where name = '"+filename+"';"
    execute_query(connection, my_queue)

# check whether input order is match the order in db
def decrypt_order_validation(connection, filename, order):
    encrypt_order = get_encrypt_order(connection,filename)
    if encrypt_order == order:
        return True
    return False

# connection = make_connection()
# create_tables(connection)
