from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Jerv.config import db_connector

engine = create_engine(db_connector, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Model = declarative_base()
Model.query = db_session.query_property()


def drop_all():
    Model.metadata.drop_all(bind=engine)


def init_db():
    import Jerv.models.site
    import Jerv.models.page
    Model.metadata.create_all(bind=engine)


def fill_data():
    from Jerv.models.site import Site
    from Jerv.models.page import Page
    a = Site("bloggurat.net")
    a.last_crawled = "2016-09-26 23:17:14.723317"
    page = Page("/", 1337)
    a.pages.append(page)
    db_session.add(a)
    db_session.commit()
