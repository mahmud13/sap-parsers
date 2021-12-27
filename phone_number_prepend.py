# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import math
import re
from pandas import ExcelWriter
from pandas import ExcelFile


# %%
file_path1 = './inputs/Otherss-2020-10-12.xlsx'
df1 = pd.read_excel(file_path1)
df1

def get_score(row, section):
    phone = row[section]
    if not phone or phone == '.' or (not isinstance(phone, str) and math.isnan(phone)):
        return ""
    phone = str(phone)
    if ',' in phone:
        parts = [p.strip() for p in phone.split(',')]
        phone = ", ".join(
            [("+" if p.startswith("88") else "") + p for p in parts])
    elif '|' in phone:
        parts = [p.strip() for p in phone.split('|')]
        phone = ", ".join(
            [("+" if p.startswith("88") else "") + p for p in parts])
    else:
        phone = ("+" if phone.startswith("88") else "") + phone
    return phone


df1['phone'] = df1.apply(
    lambda row: get_score(row, 'phone'), axis=1, result_type='expand')

#%%

def get_affilications(row, section):
    mem = row["memberships"]
    if not isinstance(mem, str):
        return ""
    all = [m.strip() for m in mem.split(",")]
    affs = []
    ships = []
    if 'BGMEA' in  all:
        ships.append('BGMEA')
    if 'BKMEA' in  all:
        ships.append('BKMEA')
    if 'National Initiative' in  all:
        ships.append('BKMEA')
    if 'Accord' in  all:
        print("here")
        affs.append('Accord')
        print(affs)
    if 'Alliance' in  all:
        affs.append('Alliance')
    if section == 'affiliations':
        print(", ".join(affs))
        return ", ".join(affs)
    else:
        return ", ".join(ships)

df1['membership'] = df1.apply(
    lambda row: get_affilications(row, 'memberships'), axis=1, result_type='expand')

df1['affiliations'] = df1.apply(
    lambda row: get_affilications(row, 'affiliations'), axis=1, result_type='expand')
#%%
df2 = df1[df1['brands'].notnull()]
df3 = df2[df2['brands'].str.contains("Matalan")]
# df1 = df1.query('phone = Man')


# %%
def get_link(row):
    print(row)
    id = row['id']
    return "https://map.rmg.org.bd/" + str(id)
df3['MiB Link'] = df3.apply(lambda  row: get_link(row), axis=1, result_type='expand')
output_path = "./outputs/factory list.xlsx"
df3.to_excel(output_path)

# %%
