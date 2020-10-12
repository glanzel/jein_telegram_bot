import settings_local
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = settings_local.dbuser
dbname = settings_local.dbname
pw = settings_local.dbpassword

dbstring = 'mysql://'+ username +':' + pw + '@localhost/' + dbname
engine = create_engine(dbstring)
Session = sessionmaker(bind=engine)

Base = declarative_base()