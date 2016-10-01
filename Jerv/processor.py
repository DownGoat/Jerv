import re
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from Jerv import logger
from Jerv.config import TDLS, LANGUAGE
from Jerv.database import db_session
from Jerv.models.found import Found
from Jerv.models.page import Page
from Jerv.models.site import Site
from langdetect import detect
import hashlib


__author__ = 'puse'


def fill_meta(page, response, response_time):
    page.http_status = response.status_code
    page.size = len(response.text)
    page.response_time = response_time

    db_session.flush()


def not_responding(site, page):
    site.status = -1
    page.status = -1
    db_session.flush()


def get_https_info(site, http_res):
    site.ocsp = http_res.get("OCSP")
    site.clssuers = http_res.get("calssuers")
    site.crlDistributionPoints = http_res.get("crlDistributionPoints")
    site.issuer = http_res.get("issuer")
    site.notAfter = http_res.get("notAfter")
    site.notBefore = http_res.get("notBefore")
    site.serialNumber = http_res.get("serialNumber")
    site.subject = http_res.get("subject")
    site.subjectAltName = http_res.get("subjectAltName")
    site.version = http_res.get("version")

    db_session.flush()


def get_page_language(soup, site):
    """
    This page attempts to get the language of the page. It looks for the html attributes land, and xml:lang.
    If this fails it checks the TDL, if that fails it tries to detect the language by looking at the text using
    the langdetect module.

    :param soup:
    :param site:
    :return:
    """
    page_language = None

    for tag in soup.findAll("html"):
        page_language = tag.get("lang")
        if page_language is None:
            page_language = tag.get("xml:lang")

    if page_language != LANGUAGE:
        tdl = site.domain.split(".")
        if len(tdl) and tdl[-1].lower() in TDLS:
            page_language = LANGUAGE
        else:
            try:
                page_language = detect(soup.get_text())
            except Exception as error:
                logger.debug(error)
                page_language = "unknown"

    if page_language.lower() != "no":
            return None

    return page_language


def build_full_path(parsed_url):
    if parsed_url.query != "":
        return "{0}?{1}".format(parsed_url.path, parsed_url.query)
    return parsed_url.path


def add_page_external(current_site, parsed_url):
    """
    This function adds a external site, and page to the database, An external page is a page on a different domain than
    the domain it was found on.

    :param current_site:
    :param parsed_url:
    :return:
    """
    external_site = Site.query.filter(Site.domain == parsed_url.netloc.lower()).first()

    if external_site is None:
        external_site = Site(parsed_url.netloc.lower())

        m = hashlib.sha1()
        joined = parsed_url.path.encode('utf-8') + parsed_url.query.encode('utf-8')
        m.update(joined)
        page_hash = m.hexdigest()

        page = Page(build_full_path(parsed_url), page_hash)
        page.found_on.append(Found(current_site.id))
        external_site.pages.append(page)

        db_session.add(external_site)
        db_session.flush()

        return

    m = hashlib.sha1()
    joined = parsed_url.path.encode('utf-8') + parsed_url.query.encode('utf-8')
    m.update(joined)
    page_hash = m.hexdigest()
    page_exists = Page.query.filter(Page.site_id == external_site.id, Page.page_hash == page_hash).first()

    if page_exists is None:
        page = Page(build_full_path(parsed_url), page_hash)
        page.found_on.append(Found(current_site.id))
        external_site.pages.append(page)

    else:
        page_exists.found_on.append(Found(current_site.id))

    db_session.flush()


def add_page_internal(current_site, parsed_url):
    m = hashlib.sha1()
    joined = parsed_url.path.encode('utf-8') + parsed_url.query.encode('utf-8')
    m.update(joined)
    page_hash = m.hexdigest()

    page_exists = Page.query.filter(Page.site_id == current_site.id, Page.page_hash == page_hash).first()

    if page_exists is None:
        page = Page(build_full_path(parsed_url), page_hash)
        current_site.pages.append(page)

        db_session.flush()


def process(site, page, response, response_time, https_res):
    if response is None:
        # If page is not responding, there is not much to save.
        logger.info("{0} not responding.".format(site.domain))
        not_responding(site, page)
        return

    logger.debug("Page {0} Content-Type: {1}".format(response.url, response.headers.get("Content-Type")))
    if "html" not in response.headers.get("Content-Type", "None"):
        logger.debug("Not parsing, response is probably not HTML")
        return

    fill_meta(page, response, response_time)

    soup = BeautifulSoup(response.text, 'html.parser')

    language = get_page_language(soup, site)
    if language is None:
        logger.info("Site is probably not norwegian.")
        return
    site.language = language

    logger.info("Probably norwegian")

    if https_res:
        get_https_info(site, https_res)

    for link in soup.findAll("a"):
        if link.has_attr('href'):
            parsed = urlparse(link["href"])

            if parsed.netloc != "" and parsed.netloc.lower() != site.domain:
                add_page_external(site, parsed)

            elif parsed.netloc == "" or parsed.netloc.lower() == site.domain:
                add_page_internal(site, parsed)
