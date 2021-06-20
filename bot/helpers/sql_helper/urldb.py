import pickle
import threading
from sqlalchemy import Column, Integer, String, LargeBinary
from bot.helpers.sql_helper import BASE, SESSION


class uRLID(BASE):
    __tablename__ = "uRLID"
    chat_id = Column(Integer, primary_key=True)
    url_id = Column(String)


    def __init__(self, chat_id, url_id):
        self.chat_id = chat_id
        self.url_id = url_id 

uRLID.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def _set(chat_id, url_id):
    adder = SESSION.query(uRLID).get(chat_id)
    if adder:
        adder.url_id = url_id
    else:
        adder = uRLID(
            chat_id,
            url_id
        )
    SESSION.add(adder)
    SESSION.commit()



def search_url(chat_id):
    try:
        return SESSION.query(uRLID).filter(uRLID.chat_id == chat_id).one().url_id
    except:
        return 'NOON'
    finally:
        SESSION.close()


def _clear(chat_id):
    rems = SESSION.query(uRLID).get(chat_id)
    if rems:
        SESSION.delete(rems)
        SESSION.commit()