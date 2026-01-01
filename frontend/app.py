import os
import socket
from flask import Flask, render_template
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    ip_address = socket.gethostbyname(os.environ["API_HOST"])
    return render_template("index.html", ip_address=ip_address, port=os.environ["API_PORT"])


if __name__ == "__main__":
    app.run(port=5001)
