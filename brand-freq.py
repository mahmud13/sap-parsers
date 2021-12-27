# %%

import pandas as pd
import numpy as np
import json
import math
import re

# %%


def to_array(data):
    return data.split('|')


def to_my_array(data):
    data = data[1:len(data) - 1]
    data = data.split(',')
    data = list(dict.fromkeys(data))
    for i in range(len(data)):
        l = len(data[i])
        d = data[i]
        if l > 2:
            data[i] = d[1:l-1]
        if data[i] == 'Local':
            data[i] = 'Local customer'
    try:
        data.remove("customer")
    except:
        pass
    return data


file_path1 = './inputs/dvv-all.csv'
published = pd.read_csv(file_path1, converters={
    'Brands': to_array,
    'Brands Customers Other': to_my_array
})
# %%
published = published.explode('Brands Customers Other')
frequency = published['Brands Customers Other'].value_counts()
# %%
output_path = "./outputs/map_all.csv"
frequency.to_csv(output_path)


# %%
