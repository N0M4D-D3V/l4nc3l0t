from pymongo import MongoClient


class DatabaseSingletonService:
    _instance = None

    def __init__(self):
        if DatabaseSingletonService._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DatabaseSingletonService._instance = MongoClient('localhost')

    @staticmethod
    def get_instance():
        if DatabaseSingletonService._instance is None:
            DatabaseSingletonService()
        return DatabaseSingletonService._instance
