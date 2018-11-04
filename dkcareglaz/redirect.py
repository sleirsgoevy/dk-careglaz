from urllib.request import urljoin
import bottle

BASE_URL = None

def redirect(url):
    if BASE_URL == None:
        bottle.redirect(url)
    else:
        bottle.redirect(urljoin(BASE_URL, url))

try: from .config import redirect_base_url as BASE_URL
except ImportError: pass
