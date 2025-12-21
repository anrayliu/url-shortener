from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from database import Database
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

db = Database()
db.connect()

CORS(app)


def hash_url(url):
    return str(hash(url))


@app.route("/api/v1/shorten", methods=["POST"]) 
def handle_shorten():
    long_url = request.get_json().get("url")

    # saved long_url, short_url pair in database
    db_pair = db.query("SELECT * FROM urls WHERE long_url = %s;", args=(long_url,))

    if db_pair is None:
        short_url = hash_url(long_url)
        db.query("INSERT INTO urls VALUES (%s, %s);", args=(long_url, short_url))
    else:
        short_url = db_pair[1]

    data = {
        "data": {
            "longUrl": long_url,
            "shortUrl": short_url
        }
    }

    return jsonify(data)

@app.route("/api/v1/redirect/<url>")
def handle_redirect(url):
    db_pair = db.query("SELECT * FROM urls WHERE short_url = %s;", args=(url,))

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
    app.run(port=5000, debug=True)
