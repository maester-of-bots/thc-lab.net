import psycopg2
from datetime import *
import random
import os
from dotenv import load_dotenv
import psycopg2.extras


class db:
    def __init__(self):
        load_dotenv()
        self.server = os.getenv('cloud_db-URL')
        self.user = os.getenv('cloud_db-User')
        self.password = os.getenv('cloud_db-Key')
        self.port = os.getenv('cloud_db-Port')
        self.database = os.getenv('cloud_db-db')
        self.sslmode = os.getenv('cloud_db-ssl')

        # self.drop_table('openai_usage')



    def get_db(self):
        # connect to MySQL server
        conn = psycopg2.connect(
            dbname=self.database,
            user=self.user,
            password=self.password,
            host=self.server,
            port=25060,)
            #sslmode='require')

        return conn


    def post_url(self, url):
        table = "urls_thc"
        column = "original_url"

        if self.get_url(url):
            pass
        else:
            conn = self.get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute(f"INSERT INTO {table} ({column}) VALUES ('{url}')")
            conn.commit()
            cur.close()
            conn.close()

    def get_url(self, url):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM urls_thc WHERE original_url LIKE '{url}'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def get_url_for_redirect(self,original_id):

        conn = self.get_db()
        cur = conn.cursor()

        cur.execute(f"SELECT original_url, clicks FROM urls_thc WHERE id = ('{original_id}')")

        data = cur.fetchone()
        url_to_return = data[0]
        clicks = data[1]

        cur.execute(f"UPDATE urls_thc SET clicks = {clicks+1} WHERE id = {original_id}")

        conn.commit()
        conn.close()
        return url_to_return


    def dump_info(self, table, bot_dict):
        conn = self.get_db()
        cur = conn.cursor()

        columns = ", ".join(bot_dict.keys())

        vals = ", ".join(["%s"]*len(bot_dict.keys()))

        cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({vals})", tuple(bot_dict.values()))
        conn.commit()
        # Close communication with the database
        cur.close()
        conn.close()

    def get_info(self, table):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

DB=db()