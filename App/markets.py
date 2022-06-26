import pandas
from pymongo import MongoClient

from App.Data.exchange_factory import ExchangeFactory
from App.Services.balance_service import BalanceService
from App.Services.symbol_info_service import SymbolInfoService
from Models.symbol_info_model import SymbolInfo
from Utils.utils import fix_floats


def update_markets(exchange):
    client = MongoClient('localhost')
    db = client['BINANCE']
    symbol_info_service = SymbolInfoService(db['SYMBOL_INFO'])
    balance_service = BalanceService(db['BALANCES'])
    balances = exchange.fetch_balance()['info']['balances']

    for balance in balances:
        balance = fix_floats(balance)
        balance_service.update_many(balance)

    markets = exchange.fetch_markets()
    in_db = pandas.DataFrame(list(symbol_info_service.find()))
    temp = []

    if len(in_db) != 0:
        temp = list(in_db['symbol'])

    for market in markets:
        symbol_info = SymbolInfo(market)

        if len(in_db) == 0:
            symbol_info_service.insert_one(symbol_info.get_json())
        else:
            if symbol_info.symbol in temp:
                symbol_info_service.update_one(symbol_info)
                temp.remove(symbol_info.symbol)
            else:
                symbol_info_service.insert_one(symbol_info)

        if len(temp) != 0:
            for symbol in temp:
                symbol_info_service.delete_one(symbol)

    exchange = ExchangeFactory().get_instance()
