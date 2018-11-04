from urllib.request import urljoin
import bottle

def redirect(url):
    bottle.redirect(bottle.request.fullpath + '/' + url)
