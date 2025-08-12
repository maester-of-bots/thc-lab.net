import psycopg2
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

        self.table = "urls"
        self.column = "original_url, base"

    def get_db(self):
        # connect to MySQL server
        conn = psycopg2.connect(
            dbname=self.database,
            user=self.user,
            password=self.password,
            host=self.server,
            port=self.port,
            sslmode=self.sslmode)
        return conn


    def post_url(self, url, domain):
        """ Post the URL to the database, generating an ID which we'll refer back to"""

        if self.get_url(url, domain):
            pass
        else:
            conn = self.get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute(f"INSERT INTO {self.table} ({self.column}) VALUES ('{url}', '{domain}')")
            conn.commit()
            cur.close()
            conn.close()

    def get_url(self, url, domain):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.table} WHERE original_url LIKE '{url}' AND base LIKE '{domain}'")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def get_url_for_redirect(self,original_id, domain):
        conn = self.get_db()
        cur = conn.cursor()
        cur.execute(f"SELECT original_url, clicks FROM {self.table} WHERE id = '{original_id}' AND base LIKE '{domain}'")
        data = cur.fetchone()
        url_to_return = data[0]
        clicks = data[1]
        cur.execute(f"UPDATE {self.table} SET clicks = {clicks+1} WHERE id = {original_id} AND base LIKE '{domain}'")
        conn.commit()
        conn.close()
        return url_to_return

DB=db()