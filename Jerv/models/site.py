import base64
import os
from sqlalchemy.orm import relationship
from Jerv.database import Model
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, UnicodeText
from Jerv.models.page import Page


__author__ = 'puse'


class Site(Model):
    __tablename__ = "site"
    id = Column("id", Integer, primary_key=True)
    domain = Column(String(512))
    indexed = Column(Boolean, default=False)
    https = Column(Boolean, default=False)
    https_checked = Column(Boolean, default=False)
    status = Column(Integer)
    last_crawled = Column(DateTime, default="2016-09-26 23:17:14.723317")
    pages = relationship("Page")

    # Cert Info
    ocsp = Column(UnicodeText())
    clssuers = Column(UnicodeText())
    crlDistributionPoints = Column(UnicodeText())
    issuer = Column(UnicodeText())
    notAfter = Column(UnicodeText())
    notBefore = Column(UnicodeText())
    serialNumber = Column(UnicodeText())
    subject = Column(UnicodeText())
    subjectAltName = Column(UnicodeText())
    version = Column(UnicodeText())
    language = Column(UnicodeText())

    def __init__(self, domain):
        self.domain = domain