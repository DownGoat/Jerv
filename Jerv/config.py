from datetime import date
import logging

db_user = "puse"
db_pass = "123qwe"
db_host = "127.0.0.1"
db_name = "jerv"
db_type = "postgresql"
db_port = "5432"
db_connector = "{0}://{1}:{2}@{3}:{4}/{5}".format(
    db_type,
    db_user,
    db_pass,
    db_host,
    db_port,
    db_name
)

logger = logging.getLogger("Jerv")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("Jerv{0}.log".format(date.today().isoformat()))
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

VERSION = "0.1"
USER_AGENT = "Mozilla/5.0 (compatible; Jerv.http.client/{0})".format(VERSION)
