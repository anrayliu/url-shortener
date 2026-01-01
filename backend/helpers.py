import hashlib


def append_http(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    return url

def get_hashed(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:7]
