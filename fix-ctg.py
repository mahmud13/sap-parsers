# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import re
from datetime import datetime

# %%
right = pd.read_csv('./inputs/CrmInput.csv', keep_default_na=False)
right

# %%
problems = [
    'officialcontact-official_phone',
    'officialcontact-official_person_phone',
    'respondent-respondent_phone',
]

today = datetime.now()
today = today.strftime("%d/%m/%Y %H:%M")
output = pd.DataFrame()
output['Name'] = right['Factory Name']
output['Website'] = right['Serial'].map(
    "https://map.rmg.org.bd/admin#/dhaka-data-process/{}".format)
output['ID'] = right['Key'].str.replace('uuid:', '')
output['Date Created'] = today
output['Date Modified'] = today
output['Modified by'] = 1
output['Created by'] = 1
output['Deleted'] = 0
output['UUID'] = right['Key'].str.replace('uuid:', '')

output

# %%

output_path = "./outputs/crm_factories.csv"
output.to_csv(output_path)


# %%
regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# %%


def verifyEmail(email):
    if re.search(regex, email):
        return True
    return False


def getEmail(email, n):
    single = n == 0
    if ',' in email:
        emails = [e.strip() for e in email.split(',')]
        if len(emails) > n:
            email = emails[n]
            single = True

    return email if single and verifyEmail(email) else ''


official = pd.DataFrame()
official['Name'] = right['Official Contact Person Name']
official['Title'] = right['Official Contact Person Designation']
official['Factory Name'] = right['Factory Name']
official['Email Address'] = right['Official Contact Person Email'].apply(
    getEmail, args=(0,))
official['Mobile'] = right['Official Contact Person Phone']
official['Office Phone'] = right['Official Contact Phone']
official['Portal User Type'] = 'Single user'
official['Type'] = 'Official'
official['Modified by'] = 1
official['Created by'] = 1
official['Deleted'] = 0
official['Factory UUID'] = right['Key'].str.replace('uuid:', '')
official['2nd Email'] = right['Official Contact Person Email'].apply(
    getEmail, args=(1,))

official['3rd Email'] = right['Official Contact Person Email'].apply(
    getEmail, args=(2,))

official

# %%

respondent = pd.DataFrame()
respondent['Name'] = right['Respondent Name']
respondent['Title'] = right['Respondent Designation']
respondent['Factory Name'] = right['Factory Name']
respondent['Email Address'] = right['Respondent Email'].apply(
    getEmail, args=(0,))

respondent['Mobile'] = right['Respondent Phone']
respondent['Office Phone'] = ''
respondent['Portal User Type'] = 'Single user'
respondent['Type'] = 'Respondent'
respondent['Modified by'] = 1
respondent['Created by'] = 1
respondent['Deleted'] = 0
respondent['Factory UUID'] = right['Key'].str.replace('uuid:', '')
respondent['2nd Email'] = right['Respondent Email'].apply(
    getEmail, args=(1,))


respondent['3rd Email'] = right['Official Contact Person Email'].apply(
    getEmail, args=(2,))

respondent


# %%
combined = pd.concat([official, respondent], ignore_index=True)
combined

# %%
output_path = "./outputs/crm_contacts.csv"
combined.to_csv(output_path)


# %%
