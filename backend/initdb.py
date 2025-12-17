from database import Database
from dotenv import load_dotenv


def populate_db():
    db = Database()
    db.connect()

    db.query("DROP TABLE IF EXISTS urls;")

    db.query('''
                CREATE TABLE urls (
                    long_url text PRIMARY KEY,
                    short_url text NOT NULL
                );
                ''')
    
    db.close()


if __name__ == "__main__":
    load_dotenv()
    populate_db()
