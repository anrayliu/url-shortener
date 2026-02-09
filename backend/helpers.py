import hashlib
import random
import logging
import string
from typing import Optional, Any, Sequence, Tuple

import psycopg2
from flask import abort


logger = logging.getLogger(__name__)

def append_http(url: str) -> str:
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

# grabs an available connection from the pool
def get_connection(pool: "psycopg2.pool.SimpleConnectionPool") -> "psycopg2.extensions.connection":
    try:
        conn = pool.getconn()
    except psycopg2.pool.PoolError as e:
        logger.error(e)
        abort(503, description="Connections at capacity")
    
    return conn

def exec_query(conn: "psycopg2.extensions.connection", query: str, args: Optional[Sequence[Any]] = None, fetch: bool = True) -> Optional[Tuple[Any, ...]]:
    with conn.cursor() as cur:
        try:
            cur.execute(query, args)
        except psycopg2.Error as e:
            conn.rollback()
            logger.error(e)
            abort(500)
        
        if fetch:
            return cur.fetchone()

def hash_url(url: str, conn: "psycopg2.extensions.connection") -> str:
    exists = True

    while exists:
        # short url is the first 7 digits in a sha256 hash
        sha = hashlib.sha256(url.encode("utf-8")).hexdigest()[:7]
        exists = exec_query(conn, "SELECT * FROM urls WHERE short_url = %s;", (sha,)) is not None
        
        # adds a random letter to the long url if hash is a conflict
        url += random.choice(string.ascii_letters)

    return sha
