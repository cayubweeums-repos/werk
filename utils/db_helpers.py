# Collection of helpers to interact with DB
import os
import pymongo
from pymongo import MongoClient
import logging

# DB system interactions
def connect_db(collection: str):
    host = os.getenv('HOST_IP')
    # Client Connection
    client = MongoClient(f"mongodb://root:example@{host}:27017/") # TODO placeholder creds
    # Database
    database = client['werk']
    # Collection
    collection = database[collection]
    return [client, database, collection]

def close_db(client: MongoClient):
    client.close()

def insert_db(collection: str, data: dict):
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
    
    
    
# User administration

def create_user(collection, username, password):
    return

def check_if_user_exists(collection, username) -> bool:
    return

def auth_user(collection, username, password) -> bool:
    return