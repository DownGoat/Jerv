from Jerv.config import logger
from Jerv.models.site import Site
from Jerv.fetcher import *
from Jerv.processor import process

__author__ = 'puse'

logger.info("Jerv starting up.")


def run():
    while True:
        sites = Site.query.filter(Site.indexed == False).all()
        for site in sites:
            for page in site.pages:
                if site.last_crawled + datetime.timedelta(minutes=1) < datetime.datetime.now():
                    process(*fetch(site, page))
                else:
                    logger.info("Visited recently, must wait a minute before requesting a new page: {0}".format(
                        site.domain))
