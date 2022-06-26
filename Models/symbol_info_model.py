import json

from pandas import DataFrame


class SymbolInfo:
    def __init__(self, market: DataFrame):
        self.id = market['id']
        self.symbol = market['symbol']
        self.precision = market['precision']
        self.minNotional = market['info']['filters'][3]['minNotional']
        self.ask = 0
        self.bid = 0
        self.mid_price = 0

    def get_json(self):
        return json.dumps(self)

