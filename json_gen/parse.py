import json
from textwrap import indent

import pandas

from config.config import BarConfig, LineConfig

def parse_json_to_config(file):
    with open(file, 'r') as f:
        data = json.load(f)

    if data['chart_type'] == "line chart":
        data_df = pandas.read_csv(data['path'], usecols=[0,1])

        raw_x = data_df.iloc[:, 0].tolist()
        raw_y = data_df.iloc[:, 1].tolist()

        loaded_config = LineConfig.from_dict(data, raw_x, raw_y)

        return loaded_config
    elif data['chart_type'] == "bar chart":
        data_df = pandas.read_csv(data['path'], usecols=[0,1])

        raw_x = data_df.iloc[:, 0].tolist()
        raw_y = data_df.iloc[:, 1].tolist()

        loaded_config = BarConfig.from_dict(data, raw_x, raw_y)

        return loaded_config
    else:
        print("Error while parsed")

    return 0
