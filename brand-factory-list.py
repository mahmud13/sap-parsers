# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from urllib.parse import urlencode
import pandas as pd
import re
from pandas import ExcelWriter
from pandas import ExcelFile
import urllib


# %%
file_path1 = './inputs/Email Addresses of Brands.xlsx'
brands = pd.read_excel(file_path1, sheet_name='brands')
brands

# %%
file_path1 = './inputs/mapped-brands.csv'
mapBrands = pd.read_csv(file_path1)
mapBrands

# %%
file_path1 = './inputs/Published Factories.xlsx'
factories = pd.read_excel(file_path1, sheet_name='output', converters={'brands': str})
factories['brands'] = factories['brands'].fillna('')
factories['brands'] = factories['brands'].str.split(pat=', ')

factories = factories.explode('brands')
factories

# %%
def get_factories(brand_name):
    fs = factories.loc[factories['brands'].apply(lambda b: brand_name in b)]
    output = ''
    for index, row in fs.iterrows():
        output = '||'.join(filter(None, [output, row['name']]))
        output = '|'.join([output, str(row['id'])])
    return output

def get_brand(brand_name):
    fs = mapBrands.loc[mapBrands['name'].str.lower() == brand_name.lower()]
    if len(fs.index) == 1:
        return fs.iloc[0]['name']
    if len(fs.index) == 0:
        return ''
    print(fs)
    print('error')
    return ''

def get_url(brand_name):
    if not brand_name:
        return ''
    return "https://map.rmg.org.bd/?" + urllib.parse.quote(urlencode({'brands': brand_name}))

brands['nameInMap'] = brands['Name'].apply(
    lambda x: get_brand(x))
brands['factories'] = brands['Name'].apply(
    lambda x: get_factories(x))

brands['url'] = brands['nameInMap'].apply(
    lambda x: get_url(x))

brands

# %%


brands1 = brands[brands['url'].astype(bool) & brands['factories'].astype(bool)]
output_path = "./outputs/brands-factories.csv"
brands1.to_csv(output_path)
brands1
# %%
