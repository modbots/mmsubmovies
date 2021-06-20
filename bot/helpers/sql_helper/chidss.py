import threading
from sqlalchemy import Column, Integer, String, LargeBinary
from bot.helpers.sql_helper import BASE, SESSION


class chidByuserid(BASE):
    __tablename__ = "chidByuserid"
    msg_idS = Column(Integer, primary_key=True)
    url_idS = Column(String)


    def __init__(self, msg_idS, url_idS):
        self.msg_idS = msg_idS
        self.url_idS = url_idS 

chidByuserid.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def _set(msg_idS, url_idS):
    adder = SESSION.query(chidByuserid).get(msg_idS)
    if adder:
        adder.url_idS = url_idS
    else:
        adder = chidByuserid(
            msg_idS,
            url_idS
        )
    SESSION.add(adder)
    SESSION.commit()



def search_url(msg_idS):
    try:
        return SESSION.query(chidByuserid).filter(chidByuserid.msg_idS == msg_idS).one().url_idS
    except:
        return 'mmsub.co'
    finally:
        SESSION.close()


