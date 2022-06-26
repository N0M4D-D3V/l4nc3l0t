import ccxt

from Utils.utils import get_keys


class ExchangeFactory:

    def __init__(self, exchange='binance'):
        self.exchange_name = exchange
        self._keys = get_keys()

    def get_instance(self):
        if self.exchange_name == 'binance':
            return ccxt.binance({
                'apiKey': self._keys.public,
                'secret': self._keys.secret,
                'enableRateLimit': True,
                'timeout': 3000,
                'options': {
                'defaultType': 'spot'
                    }
                })
        else:
            print('Exchange not supported =/')
