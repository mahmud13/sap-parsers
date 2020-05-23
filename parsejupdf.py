# %%
from PIL import Image
import PyPDF2
import sys
import glob
import os
import pdftotext
import sqlite3
import random
import string
from peewee import SqliteDatabase, Model, CharField, DoesNotExist, ForeignKeyField, DateField, IntegerField
from datetime import datetime
db = SqliteDatabase("./outputs/jubof.db")


class Cadre(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'cadres'


class BcsBatch(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'bcs_batches'


class JuBatch(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'ju_batches'


class JuDept(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'ju_depts'


class JuHall(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'ju_halls'


class HomeDistrict(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'districts'


class BloodGroup(Model):
    name = CharField()

    class Meta:
        database = db
        db_table = 'blood_groups'


class Member(Model):
    name = CharField()
    designation = CharField()
    posting_place = CharField()
    bcs_batch = ForeignKeyField(BcsBatch, column_name="bcs_batch_id")
    ju_batch = ForeignKeyField(JuBatch, column_name="ju_batch_id")
    ju_dept = ForeignKeyField(JuDept, column_name="ju_dept_id")
    ju_hall = ForeignKeyField(JuHall, column_name="ju_hall_id")
    home_district = ForeignKeyField(
        HomeDistrict, column_name="home_district_id")
    date_of_birth = DateField()
    blood_group = ForeignKeyField(BloodGroup, column_name="blood_group_id")
    cadre = ForeignKeyField(Cadre, column_name='cadre_id')
    email = CharField()
    mobile = CharField()
    image = CharField()
    serial = IntegerField()

    class Meta:
        database = db
        db_table = 'members'


db.connect()
db.create_tables([Cadre, BcsBatch, JuBatch, JuDept,
                  JuHall, HomeDistrict, BloodGroup, Member])

dir_path = "./inputs/pdfs"


# %%
for filename in os.listdir(dir_path):
    absfilename = os.path.join(dir_path, filename)
    with open(absfilename, "rb") as file:
        # read images
        serial = 0
        images = []
        input1 = PyPDF2.PdfFileReader(open(absfilename, "rb"))
        number_of_pages = input1.getNumPages()
        for page_number in range(number_of_pages):
            page0 = input1.getPage(page_number)
            if '/XObject' in page0['/Resources']:
                xObject = page0['/Resources']['/XObject'].getObject()
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        size = (xObject[obj]['/Width'],
                                xObject[obj]['/Height'])
                        data = xObject[obj]._data
                        if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                            mode = "RGB"
                        else:
                            mode = "P"
                        if '/Filter' in xObject[obj]:
                            if xObject[obj]['/Filter'] == '/FlateDecode':
                                img = Image.frombytes(mode, size, data)
                                image_name = str(serial) + '.png'
                                img.save('./outputs/jupdf/images/' +
                                         image_name)
                                images.append(image_name)
                                serial += 1
                            elif xObject[obj]['/Filter'] == '/DCTDecode':
                                image_name = str(serial) + '.jpg'
                                img = open('./outputs/jupdf/images/' +
                                           image_name, "wb")
                                img.write(data)
                                img.close()
                                images.append(image_name)
                                serial += 1
                        else:
                            img = Image.frombytes(mode, size, data)
                            image_name = str(serial) + '.png'
                            img.save('./outputs/jupdf/images/' + image_name)
                            images.append(image_name)
                            serial += 1
            else:
                print("No image found.")

        # read text
        # pdf = pdftotext.PDF(file)
        # pdf = "\n".join(pdf)
        # lines = pdf.splitlines()
        # cadre = [s.strip() for s in lines[0].split('-')][0]
        # try:
        #     dbcadre = Cadre.select().where(Cadre.name == cadre).get()
        # except DoesNotExist:
        #     dbcadre = Cadre(name=cadre)
        #     dbcadre.save()
        # member = Member()
        # serial = 0
        # for line in lines:
        #     parts = [i.strip() for i in line.split(":")]
        #     if len(parts) == 2:
        #         title = parts[0]
        #         value = parts[1]
        #         if title == 'Name':
        #             member = Member()
        #             member.cadre = dbcadre
        #             member.name = value
        #         if title == 'Designation':
        #             member.designation = value
        #         if title == 'Posting Place':
        #             member.posting_place = value
        #         if title == 'BCS Batch':
        #             try:
        #                 dbbcsbatch = BcsBatch.select().where(BcsBatch.name == value).get()
        #             except DoesNotExist:
        #                 dbbcsbatch = BcsBatch(name=value)
        #                 dbbcsbatch.save()

        #             member.bcs_batch = dbbcsbatch
        #         if title == 'JU Batch & Dept':
        #             ju = [i.strip() for i in value.split(',')]
        #             try:
        #                 dbvalue = JuBatch.select().where(
        #                     JuBatch.name == ju[0]).get()
        #             except DoesNotExist:
        #                 dbvalue = JuBatch(name=ju[0])
        #                 dbvalue.save()

        #             member.ju_batch = dbvalue
        #             try:
        #                 dbvalue = JuDept.select().where(
        #                     JuDept.name == ju[1]).get()
        #             except DoesNotExist:
        #                 dbvalue = JuDept(name=ju[1])
        #                 dbvalue.save()

        #             member.ju_dept = dbvalue
        #         if title == 'JU Hall':
        #             try:
        #                 dbvalue = JuHall.select().where(
        #                     JuHall.name == value).get()
        #             except DoesNotExist:
        #                 dbvalue = JuHall(name=value)
        #                 dbvalue.save()

        #             member.ju_hall = dbvalue
        #         if title == 'Home District':
        #             try:
        #                 dbvalue = HomeDistrict.select().where(
        #                     HomeDistrict.name == value).get()
        #             except DoesNotExist:
        #                 dbvalue = HomeDistrict(name=value)
        #                 dbvalue.save()

        #             member.home_district = dbvalue
        #         if title == 'Date of Birth':
        #             member.date_of_birth = datetime.strptime(value, '%d/%m/%Y')
        #         if title == 'Blood Group':
        #             try:
        #                 dbvalue = BloodGroup.select().where(
        #                     BloodGroup.name == value).get()
        #             except DoesNotExist:
        #                 dbvalue = BloodGroup(name=value)
        #                 dbvalue.save()

        #             member.blood_group = dbvalue
        #         if title == 'Email':
        #             member.email = value
        #         if title == 'Mobile':
        #             member.mobile = value
        #             member.image = images[serial]
        #             serial = serial + 1
        #             member.serial = serial
        #             member.save()


# %%
