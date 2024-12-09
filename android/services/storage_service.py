from abc import ABC, abstractmethod
import sqlite3
import json
import os

class StorageService(ABC):
    @abstractmethod
    async def get(self, key: str): pass
    
    @abstractmethod
    async def set(self, key: str, value: any): pass

class LocalStorageService(StorageService):
    def __init__(self):
        self.db_path = "./data/local.db"
        # self._init_db()
        
    def _init_db(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()

    async def _execute_query(self, query: str, params: tuple = None):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchone() if "SELECT" in query else None
            conn.commit()
            
            if result:
                return json.loads(result[0]) if result[0] else None
            return None
            
        finally:
            conn.close()
     
    async def get(self, key: str):
        # Async wrapper around SQLite
        return await self._execute_query(
            "SELECT value FROM config WHERE key=?", 
            (key,)
        )
    
    async def set(self, key: str, value: any):
        await self._execute_query(
            "INSERT OR REPLACE INTO config VALUES (?,?)",
            (key, json.dumps(value))
        )

    async def set_connection_config(self, config: dict, storage_type: str):
        """Store connection details and storage type locally"""
        await self.set("connection.config", config)
        await self.set("storage.type", storage_type)  # "local" or "remote"

class RemoteStorageService(StorageService):
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def get(self, key: str):
        # TODO: Implement self hosted remote storage
        pass
