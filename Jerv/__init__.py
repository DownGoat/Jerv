from Jerv.config import logger
from Jerv.models.site import Site
from Jerv.fetcher import *
from Jerv.processor import process

__author__ = 'puse'

logger.info("Jerv starting up.")


def run():
    while True:
        sites = Site.query.filter(Site.last_crawled < datetime.datetime.now() - datetime.timedelta(minutes=1)).all()
        #sites = Site.query.filter(Site.indexed == False).all()
        if len(sites) == 0:
            logger.critical("No new sites to crawl")
        for site in sites:
            if site.last_crawled + datetime.timedelta(minutes=1) < datetime.datetime.now():
                for page in site.pages:
                    if not page.indexed:
                        #try:
                        process(*fetch(site, page))
                        db_session.commit()
                        break
                        #except Exception as error:
                        #    logger.critical("Unknown Exception:")
                        #    logger.critical(error)

            else:
                logger.info("Visited recently, must wait a minute before requesting a new page: {0}".format(
                    site.domain))
        time.sleep(1)