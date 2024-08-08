# Collection of helpers to interact with DB
import os
import pymongo
from pymongo import MongoClient
from utils import general
import logging

# DB system interactions
def connect_db(collection: str):
    # Client Connection
    client = MongoClient(f"mongodb://root:example@192.168.29.45:27017/") # TODO placeholder creds
    # Database
    database = client['werk']
    # Collection
    collection = database[collection]
    return [client, database, collection]

def insert_db(database: str, collection: str, init_data: dict, log):
    # Client Connection
    try:
        client = MongoClient(f"mongodb://root:example@192.168.29.45:27017/")
    except:
        log.error(f'Unable to connecto to MongoDB at 192.168.29.45:27017')
    
    # Check if the database already exists
    if database not in client.list_database_names():
        # If not, create the database by creating a collection
        db = client[database]
        collection = db[collection]
        collection.insert_one(init_data)
        log.info(f'Successfully created database {database} with collection {collection} with initial data {init_data}')
    else:
        log.info(f"Database '{database}' already exists.")
        
def insert_row(collection: str, data: dict):
    conn = connect_db(collection)
    insert_result = conn[2].insert_one(data)
    close_db(conn[0])

def get_row_db(collection, key: str, value: str):
    conn = connect_db(collection)
    return_me = conn[2].find_one({key: value})
    close_db(conn[0])
    return return_me

def get_all_rows_db(collection) -> list:
    return list(collection.find())

def update_row_db(collection, filter, update):
    collection.update_one(filter, {"$set": update})
    
def close_db(client: MongoClient):
    client.close()
    
    
# User administration

def create_user(collection, username, password):
    return

def check_if_user_exists(collection, username, log) -> bool:
    try:
        get_row_db(collection, 'username', username)
        return True
    except:
        log.warn(f'Username {username} does not exist in the collection {collection}')
        return False

def auth_user(collection, username, password, current_session) -> bool:
    user_row = get_row_db(collection, 'username', username)
    print(user_row)
    if general.check_passwords(password, user_row['password']):
        print("Authentication successful")
        
        user_row['authenticated_sessions'].append(current_session)
        return True
    else:
        print("Authentication failed: Incorrect password")
        return False
