from Jerv.database import Model
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

__author__ = 'puse'


class Page(Model):
    __tablename__ = "page"
    id = Column("id", Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("site.id"))
    path = Column(String(1024))
    size = Column(Integer)
    response_time = Column(Integer)
    http_status = Column(Integer)
    status = Column(Integer)
    found_on = Column(Integer)
    last_crawled = Column(DateTime, default="2016-09-26 23:17:14.723317")

    def __init__(self, path, found_on, size=0, response_time=0, http_status=0, status=0):
        self.path = path
        self.found_on = found_on
        self.size = size
        self.response_time = response_time
        self.http_status = http_status
        self.status = status
