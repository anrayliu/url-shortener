from psycopg2.pool import SimpleConnectionPool
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

pool = SimpleConnectionPool(
    1, 20,
    database=os.environ["DB_NAME"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"]
)

app = Flask(__name__)

CORS(app)

def hash_url(url):
    return str(hash(url))

@app.route("/api/v1/shorten", methods=["POST"]) 
def handle_shorten():
    long_url = request.get_json().get("url")

    conn = pool.getconn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM urls WHERE long_url = %s;", (long_url,))

    # saved long_url, short_url pair in database
    db_pair = cur.fetchone()

    if db_pair is None:
        short_url = hash_url(long_url)

        cur.execute("INSERT INTO urls VALUES (%s, %s);", (long_url, short_url))
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
    conn = pool.getconn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM urls WHERE short_url = %s;", (url,))

    db_pair = cur.fetchone()

    pool.putconn(conn)

    if db_pair is None:
        response = {"error":{
            "code": 400, 
            "message": "Short URL does not exist."
        }}
        return jsonify(response)

    redirect_url = db_pair[0]
    if not redirect_url.startswith("http://") and not redirect_url.startswith("https://"):
        redirect_url = "http://" + redirect_url

    return redirect(redirect_url)

@app.route("/<url>")
def handle_main(url):
    return redirect(f"/api/v1/redirect/{url}")


if __name__ == "__main__":
    app.run(port=5000)
