from pymongo.collection import Collection


class BalanceService:
    def __init__(self, cursor: Collection):
        self.cursor = cursor

    def update_many(self, balance):
        query = {'assets': balance['assets']}
        update = {'$set': balance}
        self.cursor.update_many(query, update, True)
