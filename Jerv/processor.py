import re
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from Jerv import logger
from Jerv.database import db_session
from Jerv.models.page import Page
from Jerv.models.site import Site

__author__ = 'puse'


def fill_meta(page, res, response_time):
    page.http_status = res.code
    page.size = len(res.data)
    page.response_time = response_time

    db_session.commit()


def not_responding(site, page):
    site.status = -1
    page.status = -1
    db_session.commit()


def process(site, page, res, response_time, https_res):
    if res is None:
        # If page is not responding, there is not much to save.
        logger.info("{0} not responding.".format(site.domain))
        not_responding(site, page)
        return

    fill_meta(page, res, response_time)

    pages = set()
    external = dict()
    for link in BeautifulSoup(res.data, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr("href"):
            parsed = urlparse(link["href"])
            if parsed.netloc == "" and (parsed.path != "" or parsed.query != ""):
                if parsed.query != "":
                    pages.add("{0}?{1}".format(parsed.path, parsed.query))
                else:
                    pages.add(parsed.path)
            elif parsed.netloc != "":
                if external.get(parsed.netloc) is None:
                    external[parsed.netloc] = set()

                external[parsed.netloc].add(parsed.path)

    site.indexed = True
    for key, value in external.items():
        existing = Site.query.filter(Site.domain == key).first()
        if existing is None:
            existing = Site(key)

        for page in value:
            p = re.compile('/.*;base64', re.IGNORECASE)
            if re.search(p, page) is not None:
                logger.info("Passing link because of base64 encode media.")
                continue

            existing.pages.append(Page(page, site.id))
        db_session.add(existing)

    db_session.commit()