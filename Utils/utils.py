import pandas as pd

# Recursive function which transforms strings on floats inside a list or a dictionary.
from Config.constants import KEYS_PATH
from Models.keys_model import Keys


def fix_floats(data):
    if isinstance(data, list):
        iterator = enumerate(data)
    elif isinstance(data, dict):
        iterator = data.items()
    else:
        raise TypeError('can only traverse list or dict')

    for i, value in iterator:
        if isinstance(value, (list, dict)):
            fix_floats(value)
        elif isinstance(value, str):
            try:
                data[i] = float(value)
            except ValueError:
                pass
    return data


def get_keys() -> Keys:
    keys = pd.read_csv(KEYS_PATH, header=0)
    return Keys(keys)
