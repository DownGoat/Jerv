from sqlalchemy.orm import relationship
from Jerv.database import Model
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

__author__ = 'puse'


class Found(Model):
    __tablename__ = "found"
    id = Column("id", Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey("page.id"))
    page_external = Column(Integer)

    def __init__(self, page_external):
        self.page_external = page_external

