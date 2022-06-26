from pandas import DataFrame


class Keys:
    def __init__(self, csv_info: DataFrame):
        self.public = csv_info['APIKEY_PUBLIC'][0]
        self.secret = csv_info['APIKEY_SECRET'][0]
