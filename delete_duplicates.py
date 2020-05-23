# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# %%
file_path1 = './inputs/Final_data.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='Sheet2')
df1

# %%
file_path1 = './outputs/Final_data Filtered.xlsx'
df2 = pd.read_excel(file_path1, sheet_name='Sheet1')
df2

# %%


def credit(row):
    student_id = row['old_id_no']
    print(student_id)
    others = df1.loc[df1['Current ID'] == student_id]
    thes = others.iloc[0]
    cr = thes["Credit Earned"]
    print(cr)
    return cr


df2["credit_earned"] = df2.apply(lambda row: credit(row), axis=1)


# %%
output_path = "./outputs/Final_data Filtered Credit.xlsx"
df2.to_excel(output_path)


# %%
