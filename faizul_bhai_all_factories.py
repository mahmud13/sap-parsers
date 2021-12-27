# %%

import pandas as pd
import numpy as np
import json
import math
import re

# %%


def to_array(data):
    return data.split('|')


def appendkey(data):
    data = str(data)
    return data if data.startswith('uuid:') else 'uuid:' + data


file_path1 = '/home/mahmud/Documents/All Factories12-05-2020.csv'
published = pd.read_csv(file_path1, converters={
    'address': json.loads,
    'workers': json.loads,
    'types': to_array,
    'memberships': to_array
})
published['uuid'] = published['uuid'].apply(appendkey)
published = pd.io.json.json_normalize(published.to_dict('records'))


def parseMember(tmp):
    if 'BGMEA' in tmp and 'BKMEA' in tmp:
        return 3
    if 'BGMEA' in tmp:
        return 1
    if 'BKMEA' in tmp:
        return 2
    else:
        return 4


address_cols = ['address_plot', 'address_ward', 'address_block',
                'address_floor', 'address_union', 'address_police', 'address_display',
                'address_village', 'address_district', 'address_postcode',
                'address_roadname', 'address_upazilla', 'address_postoffice',
                'address_roadnumber']
published['memberships'] = published['memberships'].apply(parseMember)
published = published[['name', 'uuid', 'types', 'memberships',
                       'workers_male', 'workers_female', 'workers_total'] + address_cols]


master = pd.read_excel(
    '/home/mahmud/Downloads/Combind Dataset for Research and Tech Team 28_May_2020.xlsx', sheet_name='Combind_3363')

master['uuid'] = master['uuid'].apply(appendkey)
merged = published.merge(master, left_on='uuid', right_on='uuid',
                         indicator=True, how='left')

print(merged[merged['_merge'] == 'left_only'][['uuid']])

published['Official Phone'] = merged['officialcontact:official_phone']
published['Official Contact Name'] = merged['official_contact_name']
published['Official Contact Email '] = merged['official_contact_email']
published['Official Contact Phone'] = merged['official_contact_phone']
published['Respondent Name'] = merged['respondent_name']
published['Respondent Phone'] = merged['respondent_phone']
published['Respondent Email'] = merged['respondent:respondent_email']
published['Market Type'] = merged['market_type']
published['Export Status Type'] = merged['export_status']
published['DB Serial'] = merged['DB_Serial'].astype(int)
published
# %%

onlyctg = '/home/mahmud/Documents/2020-05-27T11:07:37.451Z.csv'
all = '/home/mahmud/Documents/2020-05-27T12:25:03.893Z.csv'
all = pd.read_csv(all)
onlyctg = pd.read_csv(onlyctg)[['Key']]
ctg = onlyctg.merge(all, on='Key', how='left')


def getmembers(tmp):
    if tmp['BGMEA Exists'] and tmp['BKMEA Exists']:
        return 3
    if tmp['BGMEA Exists']:
        return 1
    if tmp['BKMEA Exists']:
        return 2
    else:
        return 4


ctg['DB Serial'] = ctg['Serial']
ctg['name'] = ctg['Factory Name']
ctg['address_display'] = ctg['Display Address']
ctg['uuid'] = ctg['Key']
ctg['types'] = ctg['Factory Type'].str.split(', ')
ctg['memberships'] = ctg.apply(getmembers, axis=1)
ctg['workers_male'] = ctg['Workers Male']
ctg['workers_female'] = ctg['Workers Female']
ctg['workers_total'] = ctg['Workers Total']
ctg['brands'] = ctg['Brands'].str.split(', ')

for col in ctg:
    if col.startswith('Address') and not col.endswith('Tags') and not col.endswith('Remarks'):
        ne_col_name = '_'.join([p.lower()
                                for p in col.split(' ', 1)]).replace(' ', '')
        ctg[ne_col_name] = ctg[col]

nctg = ctg[['name', 'uuid', 'types', 'memberships',
            'workers_male', 'workers_female', 'workers_total'] + address_cols]
nctg['Official Phone'] = ctg['Official Contact Phone']
nctg['Official Contact Phone'] = ctg['Official Contact Person Phone']
nctg['Official Contact Name'] = ctg['Official Contact Person Name']
nctg['Official Contact Email '] = ctg['Official Contact Person Email']
nctg['Respondent Name'] = ctg['Respondent Name']
nctg['Respondent Phone'] = ctg['Respondent Phone']
nctg['Respondent Email'] = ctg['Respondent Email']
nctg['Market Type'] = ctg['Market Type']
nctg['Export Status Type'] = ctg['Export Status Type']
nctg['DB Serial'] = ctg['DB Serial'].astype(int)
nctg


# %%
ng = '/home/mahmud/Downloads/R2_N.ganj 2nd Slot_195_MnE Review_20.2.20.xlsx'
ng = pd.read_excel(ng, sheet_name='N.Ganj 2nd Slot_195')
ngn = pd.DataFrame()
ngn['DB Serial'] = ng['serial']
ngn['name'] = ng['Factory Name']
ngn['address_display'] = ng['Address Display Address']
ngn['uuid'] = ng['Meta Instance ID']
ngn['types'] = ng['Factory Type'].str.split(', ')
ngn['memberships'] = ng.apply(getmembers, axis=1)
ngn['workers_male'] = ng['Workers Male']
ngn['workers_female'] = ng['Workers Female']
ngn['workers_total'] = ng['Workers Total']

ngn['Official Phone'] = ng['Official Contact Phone']
ngn['Official Contact Phone'] = ng['Official Contact Person Phone']
ngn['Official Contact Name'] = ng['Official Contact Person Name']
ngn['Official Contact Email '] = ng['Official Contact Person Email']
ngn['Respondent Name'] = ng['Respondent Name']
ngn['Respondent Phone'] = ng['Respondent Phone']
ngn['Respondent Email'] = ng['Respondent Email']
ngn['Market Type'] = ng['Market Type']
ngn['Export Status Type'] = ng['Export Status Export Status Type']
for col in ng:
    if col.startswith('Address') and not col.endswith('Tags') and not col.endswith('Remarks') and not 'Display' in col and not 'Section' in col and not 'Land Mark' in col:
        ne_col_name = '_'.join([p.lower()
                                for p in col.split(' ', 1)]).replace(' ', '')
        ngn[ne_col_name] = ng[col]

ngn

# %%
result = pd.concat([published, nctg, ngn])
result

# %%
coroactivepath = '/home/mahmud/Downloads/Final_Corona Map Data_11.5.20.csv'
corona = pd.read_csv(coroactivepath)
corona['uuid'] = corona['uuid'].apply(appendkey)
corona = corona['uuid'].to_list()


def isactive(id):
    return id in corona


result['COVID Active'] = result['uuid'].apply(isactive)
result

# %%


def strjoin(da):
    return "|".join(da)


result['types'] = result['types'].apply(strjoin)

output_path = "./outputs/brands.csv"
result.to_csv(output_path)

# %%

fmoDF = fmoDF.sort_values(by=['id'])
output_path = "./outputs/merged_data.csv"
fmoDF.to_csv(output_path)

# %%
