import os

import psycopg2
import psycopg2.pool
from flask import Flask, jsonify, redirect, request, abort
from flask_cors import CORS
from dotenv import load_dotenv
from prometheus_client import Counter

import helpers


load_dotenv()

app = Flask(__name__)

CORS(app)

# init db connections
pool = psycopg2.pool.SimpleConnectionPool(
    3, 20, # min and max connections
    database=os.environ["DB_NAME"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"]
)

request_count = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

@app.after_request
def record_metrics(response):
    endpoint = request.endpoint or "unknown"

    request_count.labels(
        request.method,
        endpoint,
        response.status_code
    ).inc()

    return response

@app.route("/api/v1/shorten", methods=["POST"]) 
def handle_shorten():
    long_url = request.get_json().get("url")
    if long_url is None:
        abort(400, description="Missing 'long_url'")

    conn = helpers.get_connection(pool)

    # find saved long_url, short_url pair in database
    db_pair = helpers.exec_query(conn, "SELECT * FROM urls WHERE long_url = %s;", (long_url,))

    if db_pair is None:
        short_url = helpers.hash_url(long_url, conn)

        db_pair = helpers.exec_query(conn, "INSERT INTO urls VALUES (%s, %s);", (long_url, short_url), fetch=False)
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
    conn = helpers.get_connection(pool)

    db_pair =  helpers.exec_query(conn, "SELECT * FROM urls WHERE short_url = %s;", (url,))

    pool.putconn(conn)

    if db_pair is None:
        abort(400, description="Short URL does not exist")

    # 301 status code will reduce server load because browsers will cache the redirected url

    return redirect(helpers.append_http(db_pair[0]), code=301)

@app.route("/<url>")
def handle_main(url):
    return redirect(f"/api/v1/redirect/{url}")


if __name__ == "__main__":
    app.run(port=5000)