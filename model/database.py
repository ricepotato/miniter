import functools
import os
import logging
import importlib
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger("app.database")


def handle_schema_import_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            log.error("schema import error.")
            raise

    return wrapper


class Singleton(type):
    """Singleton.
    @see: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.dbms = {
            "mysql": self._get_mysql_conn_str,
            "sqlite": self._get_sqlite_conn_str,
        }
        self.engine = self._create_engine()
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.base = self._get_base()

    def _create_engine(self):
        dbms = os.environ.get("DBMS")
        if dbms:
            conn_str_func = self.dbms[dbms]
            conn_str = conn_str_func()
        else:
            raise IndexError("invalid dbms. check os environment 'DBMS'")

        return create_engine(conn_str, convert_unicode=False, echo=False)

    def _get_mysql_conn_str(self):
        host = os.environ.get("DB_HOST")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        port = os.environ.get("DB_PORT")
        db = os.environ.get("DB_NAME")

        return f"mysql://{user}:{password}@{host}:{port}/{db}?charset=utf8"

    def _get_sqlite_conn_str(self):
        db_file = os.environ.get("SQLITE_DB_FILE", "db.sqlite")
        return f"sqlite:///{db_file}"

    @handle_schema_import_error
    def _get_base(self):
        schema = os.environ.get("DB_SCHEMA")
        schema_mod = importlib.import_module(schema)
        return schema_mod.Base

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            log.error("Database Error. %s", e)
            session.rollback()
        finally:
            session.close()

    def create_all(self):
        """ creates all tables. """
        try:
            self.base.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to create or connect to database: %s", e)

    def drop_all(self):
        """Drop all tables."""
        try:
            self.base.metadata.drop_all(self.engine)
        except SQLAlchemyError as e:
            log.error("Unable to drop all tables of the database: %s", e)