import psycopg2
import psycopg2.pool
from flask import Flask, jsonify, redirect, request, abort
from flask_cors import CORS
from dotenv import load_dotenv
import os # environ()
import hashlib # sha256()
import logging # getLogger()
import string # ascii_letters
import random # choice()


load_dotenv()

app = Flask(__name__)

logger = logging.getLogger(__name__)

CORS(app)

# init db connections
with app.app_context():
    pool = psycopg2.pool.SimpleConnectionPool(
        3, 20, # min and max connections
        database=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )


# grabs an available connection from the pool
def get_connection():
    try:
        conn = pool.getconn()
    except psycopg2.pool.PoolError as e:
        logger.error(e)
        abort(503, description="Connections at capacity")
    
    return conn

def exec_query(conn, query, args, fetch=True):
    with conn.cursor() as cur:
        try:
            cur.execute(query, args)
        except psycopg2.Error as e:
            conn.rollback()
            logger.error(e)
            abort(500)
        
        if fetch:
            return cur.fetchone()

def hash_url(url, conn):
    exists = True

    while exists:
        # short url is the first 7 digits in a sha256 hash
        sha = hashlib.sha256(url.encode("utf-8")).hexdigest()[:7]
        exists = exec_query(conn, "SELECT * FROM urls WHERE short_url = %s;", (sha,)) is not None
        
        # adds a random letter to the long url if hash is a conflict
        url += random.choice(string.ascii_letters)

    return sha

@app.route("/api/v1/shorten", methods=["POST"]) 
def handle_shorten():
    long_url = request.get_json().get("url")
    if long_url is None:
        abort(400, description="Missing 'long_url'")

    conn = get_connection()

    # find saved long_url, short_url pair in database
    db_pair = exec_query(conn, "SELECT * FROM urls WHERE long_url = %s;", (long_url,))

    if db_pair is None:
        short_url = hash_url(long_url, conn)

        db_pair = exec_query(conn, "INSERT INTO urls VALUES (%s, %s);", (long_url, short_url), fetch=False)
        conn.commit()

    else:
        short_url = db_pair[1]

    pool.putconn(conn)

    data = {
        "data": {
            "longUrl": long_url,
            "shortUrl": short_url
        }
    }

    return jsonify(data)

@app.route("/api/v1/redirect/<url>")
def handle_redirect(url):
    conn = get_connection()

    db_pair =  exec_query(conn, "SELECT * FROM urls WHERE short_url = %s;", (url,))

    pool.putconn(conn)

    if db_pair is None:
        abort(400, description="Short URL does not exist")

    redirect_url = db_pair[0]
    if not redirect_url.startswith("http://") and not redirect_url.startswith("https://"):
        redirect_url = "http://" + redirect_url

    # 301 status code will reduce server load because browsers will cache the redirected url

    return redirect(redirect_url, code=301)

@app.route("/<url>")
def handle_main(url):
    return redirect(f"/api/v1/redirect/{url}")


if __name__ == "__main__":
    app.run(port=5000)
