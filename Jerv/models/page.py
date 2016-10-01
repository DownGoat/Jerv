from sqlalchemy.orm import relationship
from Jerv.database import Model
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean, UnicodeText
from Jerv.models.found import Found
__author__ = 'puse'


class Page(Model):
    """
    page_hash: The page hash is the SHA1 sum of the path (lowercase) + query (lowercase) of the page. The reason for
    this is way of identifying the page is because not all web servers are case sensitive. For looking up a page you
    should use the site ID and the hash.
    """
    __tablename__ = "page"
    id = Column("id", Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("site.id"))
    path = Column(UnicodeText)
    size = Column(Integer)
    response_time = Column(Integer)
    http_status = Column(Integer)
    status = Column(Integer)
    last_crawled = Column(DateTime, default="2016-09-26 23:17:14.723317")
    indexed = Column(Boolean, default=False)
    found_on = relationship("Found")
    page_hash = Column(String(64))

    def __init__(self, path, page_hash, size=0, response_time=0, http_status=0, status=0):
        self.path = path
        self.page_hash = page_hash
        self.size = size
        self.response_time = response_time
        self.http_status = http_status
        self.status = status
