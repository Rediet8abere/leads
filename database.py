from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_DATABASE = 'sqlite:///orm.db'
# sqlite:///orm.db
# sqlite+aiosqlite:///orm.db
# 'mysql+pymysql://root:test1234'

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
