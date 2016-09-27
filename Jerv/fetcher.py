import datetime
import http.client
import time
from Jerv import logger
from Jerv.config import USER_AGENT

__author__ = 'puse'


def check_https(site):
    https = True
    https_res = None
    try:
        conn = http.client.HTTPSConnection(site.domain, timeout=20)
        user_agent = {"User-Agent": USER_AGENT}
        conn.request("HEAD", "/", headers=user_agent)
        https_res = conn.getresponse()
    except Exception as err:
        logger.exception(err)
        https = False

    return https, https_res


def fetch(site, page):
    logger.info("Fetching: {0}".format(site.domain))

    request_start = time.time()

    conn = http.client.HTTPConnection(site.domain, timeout=20)
    user_agent = {"User-Agent": USER_AGENT}

    res = None
    try:
        conn.request("GET", page.path, headers=user_agent)
        res = conn.getresponse()
        try:
            res.data = res.read()
        except http.client.IncompleteRead as err:
            res.data = err.partial
            logger.info("Partial read from {0} on page: {1}".format(site.domain, page.path))
    except Exception as err:
        logger.exception(err)

    site.status = 1
    page.status = 1
    site.last_crawled = datetime.datetime.now()
    page.last_crawled = datetime.datetime.now()

    request_end = time.time()
    request_length = request_end - request_start

    https_res = None
    if not site.https_checked:
        site.https, https_res = check_https(site)
        site.https_checked = True

    return site, page, res, request_length, https_res
