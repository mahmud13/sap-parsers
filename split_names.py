# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# %%
file_path1 = './inputs/Fall-2020-Admission-Data-Full_19 Oct 20.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='data-1603090623775')
df1


# %%
def get_first_name(row):
    full_name = row["full_name"]
    split_name = full_name.split(" ")
    return split_name[0]


def get_middle_name(row):
    full_name = row["full_name"]
    split_name = full_name.split(" ")
    if len(split_name) > 2:
        return " ".join(split_name[1:-1])
    return ""


def get_last_name(row):
    full_name = row["full_name"]
    split_name = full_name.split(" ")
    if len(split_name) > 1:
        return split_name[-1]
    return ""


df1["full_name"] = df1["student_name"].str.strip()
df1['Student First Name'] = df1.apply(
    lambda row: get_first_name(row), axis=1, result_type='expand')
df1['Student Middle Name'] = df1.apply(
    lambda row: get_middle_name(row), axis=1, result_type='expand')
df1['Student Last Name'] = df1.apply(
    lambda row: get_last_name(row), axis=1, result_type='expand')

# %%
output_path = "./outputs/output.xlsx"
df1.to_excel(output_path)


# %%
df1['DOB'] = df1['date_of_birth'].dt.strftime('%d.%m.%Y')
df1


# %%
def get_mother_first_name(row):
    if pd.isnull(row["mother_name"]):
        return ""
    full_name = row["mother_name"].strip()
    split_name = full_name.split(" ")
    if len(split_name) == 1:
        return split_name[0]
    if len(split_name) > 1:
        return " ".join(split_name[0:-1])
    return ""


def get_mother_last_name(row):
    if pd.isnull(row["mother_name"]):
        return ""
    full_name = row["mother_name"].strip()
    split_name = full_name.split(" ")
    if len(split_name) > 1:
        return split_name[-1]
    return ''


df1['mother_name'] = df1['father_name'].str.strip()
df1['Father First Name'] = df1.apply(
    lambda row: get_mother_first_name(row), axis=1, result_type='expand')
df1['Father Last Name'] = df1.apply(
    lambda row: get_mother_last_name(row), axis=1, result_type='expand')


# %%
df1["semester"] = df1["Reg. From"]
df1['session'] = df1["semester"].str.split(" ", expand=True)[0]
df1['year'] = df1["semester"].str.split(" ", expand=True)[1]
df1

# %%


def start_date(row):
    if row['session'] == 'SPRINT':
        return '01.01.' + row['year']
    if row['session'] == 'SUMMER':
        return '01.05.' + row['year']
    if row['session'] == 'FALL':
        return '01.09.' + row['year']


def end_date(row):
    if row['session'] == 'SPRINT':
        return '30.04.' + row['year']
    if row['session'] == 'SUMMER':
        return '31.08.' + row['year']
    if row['session'] == 'FALL':
        return '31.12.' + row['year']


df1["module_booked_on"] = df1.apply(lambda row: start_date(row), axis=1)
df1["module_ended_on"] = df1.apply(lambda row: end_date(row), axis=1)


# %%
