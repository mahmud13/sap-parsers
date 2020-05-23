# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


# %%
file_path1 = './inputs/factories.csv'
df1 = pd.read_csv(file_path1)
df1


# %%
gmail = 0
yahoo = 0
hotmail = 0
other = 0
other_email = []
for index, row in df1.iterrows():
    email = row["email"]
    if not isinstance(email, str):
        continue
    if email.find('gmail') >= 0:
        gmail = gmail + 1
    elif email.find('yahoo') >= 0:
        yahoo = yahoo + 1
    elif email.find('hotmail') >= 0:
        hotmail = hotmail + 1
    elif email.find('live') >= 0:
        hotmail = hotmail + 1
    else:
        other = other + 1
        other_email.append(email)
print('Gmail: ' + str(gmail))
print('Yahoo: ' + str(yahoo))
print('Hotmail: ' + str(hotmail))
print('Other: ' + str(other))
print(other_email)

# %%
