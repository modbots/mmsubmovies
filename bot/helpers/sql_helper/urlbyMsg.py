import threading
from sqlalchemy import Column, Integer, String, LargeBinary
from bot.helpers.sql_helper import BASE, SESSION


class urlBymsg(BASE):
    __tablename__ = "urlBymsg"
    msg_id = Column(Integer, primary_key=True)
    url_id = Column(String)


    def __init__(self, msg_id, url_id):
        self.msg_id = msg_id
        self.url_id = url_id 

urlBymsg.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def _set(msg_id, url_id):
    adder = SESSION.query(urlBymsg).get(msg_id)
    if adder:
        adder.url_id = url_id
    else:
        adder = urlBymsg(
            msg_id,
            url_id
        )
    SESSION.add(adder)
    SESSION.commit()



def search_url(msg_id):
    try:
        return SESSION.query(urlBymsg).filter(urlBymsg.msg_id == msg_id).one().url_id
    except:
        return 'https://google.com'
    finally:
        SESSION.close()


