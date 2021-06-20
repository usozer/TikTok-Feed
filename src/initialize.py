import logging
import json

import yaml
import pandas as pd
import sqlalchemy
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP

# Set up module logger
logger = logging.getLogger(__name__)

Base = declarative_base()


class TikTok(Base):
    """Create a table for ingredients"""

    __tablename__ = "tiktoks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shortlink = Column(String(100), unique=False, nullable=False)
    timestamp = Column(Integer, unique=False, nullable=False)

    # String representation, displays primary key
    def __repr__(self):
        return "<TikTok %r>" % self.shortlink


def create_db(engine_string, engine=None):
    """Create db at the specified engine.

    Args:
        engine_string (str): URI to engine
        engine (`sqlalchemy.engine.Engine`): specified engine object, optional
    """
    try:
        if not engine:
            engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database created at %s.", engine)
    except sqlalchemy.exc.ArgumentError:
        logger.error("Invalid engine string provided")
    # except sqlalchemy.exc.OperationalError:
    #     logger.error("Connection timed out, please check VPN connection")
    except Exception as e:
        logger.error("Unknown error", e)


def delete_db(engine_string, engine=None):
    """Delete database from provided engine.x

    Args:
        engine_string (str): URI to engine
        engine (`sqlalchemy.engine.Engine`): specified engine object, optional
    """
    try:
        if not engine:
            engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.drop_all(engine)
        logger.info("Database deleted at %s.", engine)
    except sqlalchemy.exc.ArgumentError:
        logger.error("Invalid engine string provided")
    except sqlalchemy.exc.OperationalError:
        logger.error("Connection timed out, please check VPN connection")
    except Exception as e:
        logger.error("Unknown error", e)


def initialize(args):
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # config = config["initialize"]

    create_db(args.output)

    with open(args.input, "r") as f:
        records = json.loads(f.read())

    tiktoks = []
    for record in records:
        tiktoks.append(TikTok(shortlink=record[0], timestamp=record[1]))

    engine = sqlalchemy.create_engine(args.output)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all(tiktoks)
    session.commit()

    session.close()
