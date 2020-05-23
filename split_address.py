# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import re
from pandas import ExcelWriter
from pandas import ExcelFile


# %%
file_path1 = './inputs/spring-2020-admission-data-full_18th May_iplu bhai.xlsx'
df1 = pd.read_excel(file_path1, sheet_name='data-1589814860825')
df1

# %%
file_path1 = './inputs/geo_districts.csv'
df2 = pd.read_csv(file_path1)
df2

# %%
districts = df2["district"].tolist()
districts

# %%


def get_permanent_district(row):
    address = row["permanent_address"].lower()
    print(address)
    for district in districts:
        if district == 'Chattogram' and address.find('chittagong') >= 0:
            return district
        if district == 'Chapainawabganj' and address.find('chapainababganj') >= 0:
            return district
        if district == 'Bogura' and address.find('bogra') >= 0:
            return district
        if address.find(district.lower()) >= 0:
            return district
    return ''


df1["permanent_address"] = df1["present_address"].astype('str')
df1['permanent_district'] = df1.apply(
    lambda row: get_permanent_district(row), axis=1, result_type='expand')


# %%

def get_permanent_division(row):
    district = row["permanent_district"]
    print(district)
    if district:
        res = df2.loc[df2['district'] == district]
        div = res.iloc[0].division
        return div
    return ''


df1['permanent_division'] = df1.apply(
    lambda row: get_permanent_division(row), axis=1, result_type='expand')

# %%


def get_permanent_postcode(row):
    address = row["permanent_address"]
    print(address)
    matches = re.findall(r'\b\d{4}\b', address)
    print(matches)
    return matches[-1] if len(matches) else ''


df1["permanent_address"] = df1["present_address"].astype('str')
df1['permanent_postcode'] = df1.apply(
    lambda row: get_permanent_postcode(row), axis=1, result_type='expand')


# %%
df1["country"] = "Bangladesh"
# %%
output_path = "./outputs/student_master_all.xlsx"
df1.to_excel(output_path)


# %%
def split_present_address(row, part):
    address = str(row["present_address_filtered"])
    address = re.sub(' +', ' ', address)
    address = ":".join([x.strip() for x in address.split(":")])
    address = "-".join([x.strip() for x in address.split("-")])
    address = [x.strip() for x in re.split(r",|;|\|", address)]

    address_arr = []
    cur = 0
    address_arr.append('')
    for address_part in address:
        extra_spaces = address_part.count(':') + address_part.count('-') * 2
        char_limit = 40 - extra_spaces
        if len(address_arr[cur]) + len(address_part) <= char_limit:
            address_arr[cur] = ", ".join(
                filter(None, [address_arr[cur], address_part]))
        elif len(address_part) <= char_limit:
            cur = cur + 1
            address_arr.append(address_part)
        else:
            other_parts = re.split(r'(\s+)*(?![^()]*\))', address_part)
            print(address_part)
            print(other_parts)
            for other_part in other_parts:
                if len(address_arr[cur]) + len(other_part) <= char_limit:
                    address_arr[cur] = " ".join(
                        filter(None, [address_arr[cur], other_part]))
                elif len(other_part) <= char_limit:
                    cur = cur + 1
                    address_arr.append(other_part)
                else:
                    print(other_part + ' - ' + str(len(other_part)))

    if len(address_arr) > part:
        ret_part = address_arr[part]
        ret_part = ret_part.replace(":", ": ")
        ret_part = ret_part.replace("-", " - ")
        return ret_part
    return ''


df1['present_address_filtered'] = df1['present_address'].str.replace(
    "_x000D_\n", ", ")
df1['present_address_filtered'] = df1['present_address_filtered'].str.replace(
    "_x005F", "")

df1['present_address_filtered'] = df1['present_address_filtered'].str.replace(
    "_x005F\r\n", ", ")

df1['present_address_filtered'] = df1['present_address_filtered'].str.replace(
    "\n", ", ")
df1['present_address_filtered'] = df1['present_address_filtered'].str.replace(
    ".", " ")

for i in range(0, 6):
    df1['present_address-' + str(i+1)] = df1.apply(
        lambda row: split_present_address(row, i), axis=1, result_type='expand')

# %%


def split_permanent_address(row, part):
    address = str(row["permanent_address_filtered"])
    address = re.sub(' +', ' ', address)
    address = ":".join([x.strip() for x in address.split(":")])
    address = "-".join([x.strip() for x in address.split("-")])
    address = [x.strip() for x in re.split(r",|;|\|", address)]

    address_arr = []
    cur = 0
    address_arr.append('')
    for address_part in address:
        extra_spaces = address_part.count(':') + address_part.count('-') * 2
        char_limit = 40 - extra_spaces
        if len(address_arr[cur]) + len(address_part) <= char_limit:
            address_arr[cur] = ", ".join(
                filter(None, [address_arr[cur], address_part]))
        elif len(address_part) <= char_limit:
            cur = cur + 1
            address_arr.append(address_part)
        else:
            other_parts = re.split(r'(\s+)*(?![^()]*\))', address_part)
            for other_part in other_parts:
                if len(address_arr[cur]) + len(other_part) <= char_limit:
                    address_arr[cur] = " ".join(
                        filter(None, [address_arr[cur], other_part]))
                elif len(other_part) <= char_limit:
                    cur = cur + 1
                    address_arr.append(other_part)
                else:
                    print(other_part + ' - ' + str(len(other_part)))

    if len(address_arr) > part:
        ret_part = address_arr[part]
        ret_part = ret_part.replace(":", ": ")
        ret_part = ret_part.replace("-", " - ")
        return ret_part
    return ''


df1['permanent_address_filtered'] = df1['permanent_address'].str.replace(
    "_x000D_\n", ", ")
df1['permanent_address_filtered'] = df1['permanent_address_filtered'].str.replace(
    "_x005F", "")

df1['permanent_address_filtered'] = df1['permanent_address_filtered'].str.replace(
    "_x005F\r\n", ", ")

df1['permanent_address_filtered'] = df1['permanent_address_filtered'].str.replace(
    "\n", ", ")
df1['permanent_address_filtered'] = df1['permanent_address_filtered'].str.replace(
    ".", " ")

for i in range(0, 6):
    df1['permanent_address-' + str(i+1)] = df1.apply(
        lambda row: split_permanent_address(row, i), axis=1, result_type='expand')

# %%
