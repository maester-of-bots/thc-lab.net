from modules.sql import *

connection = DB.get_db()
cur = connection.cursor()

with cur as cursor:
    cursor.execute(open("data/cloud.sql", "r").read())

connection.commit()
connection.close()
