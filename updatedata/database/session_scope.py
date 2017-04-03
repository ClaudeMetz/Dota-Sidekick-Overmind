from contextlib import contextmanager
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base


# Provides an easy way to handle interactions with a database

Base = declarative_base()


@contextmanager
def session_scope(language, db_name):
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".tmp", "db", language, db_name + ".db"))
    engine = create_engine("sqlite:///" + db_path)
    Base.metadata.create_all(engine)

    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
