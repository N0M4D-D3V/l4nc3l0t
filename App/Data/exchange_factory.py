import ccxt

from Utils.utils import get_keys


class ExchangeFactory:
    _instance = None

    def __init__(self, exchange='binance'):
        if ExchangeFactory._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.exchange_name = exchange
            self._keys = get_keys()
            ExchangeFactory._instance = self._get_exchange()

    @staticmethod
    def get_instance():
        if ExchangeFactory._instance is None:
            ExchangeFactory()
        return ExchangeFactory._instance

    def _get_exchange(self):
        if self.exchange_name == 'binance':
            return ccxt.binance(
                {'apiKey': self._keys.public, 'secret': self._keys.secret, 'enableRateLimit': True, 'timeout': 3000,
                    'options': {'defaultType': 'spot'}})
        else:
            print('Exchange not supported =/')
