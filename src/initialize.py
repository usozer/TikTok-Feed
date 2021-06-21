import logging
import json

import yaml
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Set up module logger
logger = logging.getLogger(__name__)

Base = declarative_base()


class TikTok(Base):
    """Create a table for links"""

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
    except Exception as e:
        logger.error("Unknown error", e)


def initialize(args):
    """Initialize database"""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # No config vars for initialize module at this time
    # config = config["initialize"]

    engine = create_db("sqlite:///" + args.output)

    with open(args.input, "r") as f:
        records = json.loads(f.read())
    
    logger.debug("Received %i records", len(records))

    tiktoks = []
    for record in records:
        tiktoks.append(TikTok(shortlink=record[0], timestamp=record[1]))

    SessionInstance = sessionmaker(bind=engine)
    session = SessionInstance()

    logger.info("Adding %i links to db %s", len(tiktoks), args.output)
    session.add_all(tiktoks)
    session.commit()
    logger.info("Successfully committed to db")

    session.close()
