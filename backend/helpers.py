import hashlib
import random
import logging
import string

import psycopg2
from flask import abort


logger = logging.getLogger(__name__)

def append_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

def get_hashed(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:7]

# grabs an available connection from the pool
def get_connection(pool):
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
        sha = get_hashed(url)
        exists = exec_query(conn, "SELECT * FROM urls WHERE short_url = %s;", (sha,)) is not None
        
        # adds a random letter to the long url if hash is a conflict
        url += random.choice(string.ascii_letters)

    return sha
