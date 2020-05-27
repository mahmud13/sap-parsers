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
file_path1 = './inputs/AdmissionMaster_app-id-student-id-personal-details-ssc-hsc-o-a-undergrad result_22-01-2020.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='specific_student_data')
df1

# %%
file_path1 = './inputs/applicant-id-with-admission-test-results-number.xlsx'
df2 = pd.read_excel(file_path1, sheet_name='applicant_marks')
df2

# %%


def get_score(row, section):
    print(row.name)
    applicant_id = row["applicant_id"]
    score = df2.loc[(df2['applicant_id'] == applicant_id)
                    & (df2['name'] == section)]
    if score.shape[0] == 0:
        return 0
    return score.iloc[0].earn_mark


sections = [
    'HIGH MATH MCQ(20)',
    'MATH MCQ(30)',
    'LOG REA MCQ(24)',
    'ENG MCQ(25)',
    'ENG COM(40)',
    'BIO and CHE(20)',
    'ARC DRA(40)',
    'ARC WRI(20)',
    'MBA LOG REA(20)',
    'MBA ENG MCQ(30)',
    'ENG ESSAY(1)',
    'MBA MATH(40)',
    'LOG REA(30)',
    'MATH(40)',
    'MS BTC ENG(1)',
    'MS BTC BIOLOGY(50)',
    'QB on CS(30)',
    'CSE ENG COM(1)',
    'MA ENG ESSAY(50)',
    'Electrical Circuit(40)',
    'MSc/MEngg EEE ENG COM(1)',
    'ENG Written(80)',
]
for section in sections:
    df1[section] = df1.apply(
        lambda row: get_score(row, section), axis=1, result_type='expand')


# %%
output_path = "./outputs/student_master_all.xlsx"
df1.to_excel(output_path)


# %%
file_path1 = './inputs/spring-2020-admission-data-full_18th May_iplu bhai.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='data-1589814860825')
df1


# %%
scores = []
for index, row in df1.iterrows():
    marks = row["result"]
    if isinstance(marks, float) and math.isnan(marks):
        continue
    split_marks = marks.split(',')
    for mark in split_marks:
        [sub, score] = mark.split('-')
        df1.at[index, sub] = score
# %%
