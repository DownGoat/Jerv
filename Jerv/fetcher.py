import datetime
import http
import requests
import time
from Jerv import logger
from Jerv.config import USER_AGENT
from urllib.parse import urljoin
from Jerv.database import db_session

__author__ = 'puse'


def check_https(site):
    https = True
    https_res = None
    try:
        conn = http.client.HTTPSConnection(site.domain, timeout=20)
        user_agent = {"User-Agent": USER_AGENT}
        conn.request("HEAD", "/", headers=user_agent)
        https_res = conn.sock.getpeercert()
    except Exception as err:
        logger.debug(err)
        https = False

    return https, https_res


def fetch(site, page):
    logger.info("Fetching: {0}".format(site.domain))

    joined_url = urljoin("http://" + site.domain, page.path)

    request_start = time.time()

    response = None
    try:
        response = requests.get(
            joined_url,
            timeout=20,
            allow_redirects=True,
            headers={"User-Agent": USER_AGENT}
        )
    except requests.exceptions.RequestException as error:
        logger.debug(error)
        logger.info("Could not fetch: {0}".format(site.domain))

    request_end = time.time()
    request_length = request_end - request_start

    site.indexed = True
    site.status = 1
    page.status = 1
    page.indexed = True
    site.last_crawled = datetime.datetime.now()
    page.last_crawled = datetime.datetime.now()

    db_session.commit()

    https_res = None
    if not site.https_checked:
        site.https, https_res = check_https(site)
        site.https_checked = True

    return site, page, response, request_length, https_res
