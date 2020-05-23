# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# %%
file_path1 = './inputs/Final_data.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='Sheet1')
df1
# %%

file_path2 = './inputs/id-program_relationship.xlsx'
df2 = pd.read_excel(file_path2, sheet_name='Sheet1', index_col='program_code')
df2


# %%
duplicates = df1.duplicated(
    subset=['old_id_no', 'semester', 'course_code'], keep=False)
data = df1[duplicates].sort_values(by=['old_id_no', 'course_code', 'semester'])
data = data.drop_duplicates(
    subset=['program', 'old_id_no', 'semester', 'course_code'], keep=False)
data


# %%
output_path = "./outputs/output4.xlsx"
data.to_excel(output_path)


# %%
for index, row in data.iterrows():
    program_id = int(str(row['old_id_no'])[-5:-3])
    if df2.loc[program_id]['program'] != row['program']:
        print(row['old_id_no'])
        df1 = df1.drop(index)


# %%
output_path = "./outputs/Final_data Filtered.xlsx"
df1.to_excel(output_path)


# %%
file_path1 = './inputs/Final_data.xlsx'
df3 = pd.read_excel(file_path1, sheet_name='Sheet2')
df3

# %%


def credit(row):
    student_id = row['old_id_no']
    print(student_id)
    others = df3.loc[df3['Current ID'] == student_id]
    thes = others.iloc[0]
    cr = thes["Credit Earned"]
    print(cr)
    return cr


df1["total_credit_earned"] = df1.apply(lambda row: credit(row), axis=1)
df1
# %%

output_path = "./outputs/Final_data Filtered Credit.xlsx"
df1.to_excel(output_path)

# %%

file_path1 = './outputs/Final_data Filtered Credit.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='Sheet1')
df1

# %%
df1['session'] = df1["semester"].str.split(" ", expand=True)[0]
df1['year'] = df1["semester"].str.split(" ", expand=True)[1]
df1

# %%


def start_date(row):
    if row['program'] == 'PHR':
        if row['session'] == 'Spring':
            return '01.01.' + row['year']
        if row['session'] == 'Summer':
            return '01.07.' + row['year']
    else:
        if row['session'] == 'Spring':
            return '01.01.' + row['year']
        if row['session'] == 'Summer':
            return '01.05.' + row['year']
        if row['session'] == 'Fall':
            return '01.09.' + row['year']


def end_date(row):
    if row['program'] == 'PHR':
        if row['session'] == 'Spring':
            return '30.06.' + row['year']
        if row['session'] == 'Summer':
            return '31.12.' + row['year']
    else:
        if row['session'] == 'Spring':
            return '30.04.' + row['year']
        if row['session'] == 'Summer':
            return '31.08.' + row['year']
        if row['session'] == 'Fall':
            return '31.12.' + row['year']


df1["module_booked_on"] = df1.apply(lambda row: start_date(row), axis=1)
df1["module_ended_on"] = df1.apply(lambda row: end_date(row), axis=1)
# %%

output_path = "./outputs/Final_data Filtered Credit Session.xlsx"
df1.to_excel(output_path)


# %%
# %%
file_path1 = './outputs/Final_data Filtered Credit Session.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='Sheet1')
df1


# %%
df1.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
df1
# %%
duplicates = df1.duplicated(
    subset=['old_id_no', 'semester', 'course_code'], keep=False)
data = df1[duplicates].sort_values(by=['old_id_no', 'course_code', 'semester'])
data.dropna(axis=0, inplace=True)
data
# %%
data = df1.drop_duplicates(
    subset=['old_id_no', 'semester', 'course_code'], keep='first')
data
# %%
output_path = "./outputs/duplicate_id_sem_course.xlsx"
data.to_excel(output_path)

# %%
output_path = "./outputs/Filtered_duplicate_id_sem_course.xlsx"
data.to_excel(output_path)


# %%
