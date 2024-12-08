import os

class StorageRepository:
    def __init__(self, storage_service):
        self._service = storage_service
    
    async def get_config(self, key: str):
        return await self._service.get(key)
        
    async def set_config(self, key: str, value: any):
        await self._service.set(key, value)
