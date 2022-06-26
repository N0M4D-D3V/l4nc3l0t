from pymongo.collection import Collection
from pymongo.cursor import Cursor

from Models.symbol_info_model import SymbolInfo


class SymbolInfoService:
    def __init__(self, cursor: Collection):
        self.cursor = cursor

    def find(self) -> Cursor:
        return self.cursor.find()

    def insert_one(self, symbol_info: SymbolInfo):
        self.cursor.insert_one(symbol_info.get_json())

    def update_one(self, symbol_info: SymbolInfo):
        query = {'symbol': symbol_info.symbol}
        update = {'$set': symbol_info.get_json()}
        self.cursor.update_one(query, update)

    def delete_one(self, symbol: str):
        query = {'symbol': symbol}
        self.cursor.delete_one(query)
