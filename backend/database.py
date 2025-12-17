import psycopg2
import os


class DatabaseNotConnected(Exception):
    pass


class Database:
    def __init__(self):
        self.connected = False
        
        self._conn = None 
        self._cur = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def connect(self):
        if not self.connected:
            self._conn = psycopg2.connect(database=os.environ["DB_NAME"],
                                host=os.environ["DB_HOST"],
                                port=os.environ["DB_PORT"],
                                user=os.environ["DB_USER"],
                                password=os.environ["DB_PASSWORD"])
            self._cur = self._conn.cursor()
            self.connected = True

    def close(self):
        if self.connected:
            self._cur.close()
            self._conn.close()
            self.connected = False

    def query(self, q, all_=False, args=None):
        if not self.connected:
            raise DatabaseNotConnected("Not connected.")

        try:
            self._cur.execute(q, args)
        except psycopg2.Error as e:
            self._conn.rollback()
            raise e
        else:
            self._conn.commit()

            if q.lower().startswith("select"):
                return self._cur.fetchall() if all_ else self._cur.fetchone()
