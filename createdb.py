#from sqlalchemy import create_engine
#engine = create_engine('mysql://trakkr:cw0103aph@localhost/telegram_bot')
#engine = create_engine('sqlite://')

from base import Session, engine, Base
from reactions import Reactions

# 2 - generate database schema
Base.metadata.create_all(bind=engine)

# 3 - create a new session
session = Session()

# 4 - create test
test = Reactions(message_id=23, value="yes", user="glanzel")
session.add(test)

session.commit()
session.close()