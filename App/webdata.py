import json
import os
import threading
import time

import numpy as np
import pandas
from unicorn_binance_websocket_api import BinanceWebSocketApiManager

from App.Services.database_singleton_service import DatabaseSingletonService
from Models.keys_model import Keys
from Utils.utils import fix_floats, get_keys


def run_websocket(symbols, channels):
    keys: Keys = get_keys()
    websocket = BinanceWebSocketApiManager(exchange="binance.com")
    websocket.create_stream(['arr'], ["!userData"], api_key=keys.public, api_secret=keys.secret,
                            stream_label='UserData')
    websocket.create_stream(channels, symbols)
    worker_thread = threading.Thread(target=print_stream, args=(websocket,))
    worker_thread.start()

    while True:
        os.system('clear')
        websocket.print_summary()
        time.sleep(5)


def print_stream(websocket):
    db_client = DatabaseSingletonService.get_instance()
    db = db_client['BINANCE']
    cursor = db['LOGGER']

    while True:
        if websocket.is_manager_stopping():
            exit(0)

        new_data = websocket.pop_stream_data_from_stream_buffer()
        if new_data is False:
            time.sleep(0.1)
        else:
            new_data = json.loads(new_data)

            if 'stream' in new_data:
                update_mid_price(db, new_data)
            elif 'executionReport' in new_data.values():
                if new_data['X'] != 'PARTIALLY_FILLED':
                    new_data['type'] = 'position'
                    new_data = fix_floats(new_data)
                    cursor.insert_one(new_data)
            elif 'outboundAccountPosition' in new_data.values():
                new_data['type'] = 'position'
                new_data = fix_floats(new_data)
                cursor.insert_one(new_data)


def update_mid_price(db, new_data):
    symbol = new_data['stream'].replace('@depth5', '').upper()
    ask = float(new_data['data']['asks'][0][0])
    bid = float(new_data['data']['bids'][0][0])
    cursor = db['SYMBOL_INFO']
    query = {'id': symbol}

    if not np.isnan(ask):
        update = {'$set': {'ask': ask}}
        cursor_update_one(query, update)

    if not np.isnan(bid):
        update = {'$set': {'bid': bid}}
        cursor_update_one(query, update)

    symbol_info = pandas.DataFrame(list(cursor.find(query)))
    ask = symbol_info['ask'][0]
    bid = symbol_info['bid'][0]
    midprice = (ask + bid) / 2

    update = {'$set': {'midprice': midprice}}
    cursor.update(query, update)
