import os.path
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

from util.overseer import tmp_path

# Provides an easy way to handle interactions with a database

Base = declarative_base()


@contextmanager
def session_scope(language):
    db_path = os.path.join(tmp_path, "db", language, "tmp.db")
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
