from modules.sql import *

connection = db().get_db()
cur = connection.cursor()

with cur as cursor:
    cursor.execute(open("cloud.sql", "r").read())

connection.commit()
connection.close()