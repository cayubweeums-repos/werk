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
        log.debug(f'Successfully created database {database} with collection {collection} with initial data {init_data}')
    else:
        log.debug(f"Database '{database}' already exists.")
        
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
    
def update_user_field_db(username, field, update, log):
    conn = connect_db('users')
    log.debug(f'Updating one field for user {username} on field {field}')
    conn[2].update_one(
        {'username': username},
        {"$set": {field: str(update)}}
    )
    
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
        log.warning(f'Username {username} does not exist in the collection {collection}')
        return False

def auth_user(collection, username, password, current_session, log) -> bool:
    log.debug('Attempting to authenticate user')
    user_row = get_row_db(collection, 'username', username)
    log.warn(f'{user_row}')
    print(user_row)
    if general.check_passwords(password, user_row['password']):
        log.debug(f"{user_row['username']} successfully authenticated")
        print("Authentication successful")
        
        update_user_field_db(username, 'authenticated_session', current_session, log)
        
        return True
    else:
        log.warning('Authentication failed: Incorrect password')
        return False


# Session Administration

def check_if_authenticated_session(session_id, log):
    log.debug(f'Checking if {session_id} is an authenticated session')
    conn = connect_db('users')
    
    user_row = conn[2].find_one({'authenticated_session': str(session_id)})
    
    if user_row:
        log.debug(f"Session ID {session_id} is active for user: {user_row['username']}.")
        return True
    else:
        log.warn(f"Session ID {session_id} is not active for any user.")
        return False
