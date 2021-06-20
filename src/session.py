import logging
from typing import List

import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from src.initialize import TikTok

logger = logging.getLogger(__name__)


class SessionManager:
    def __init__(self, engine_string):
        """
        Args:
            engine_string: str - Engine string
        """
        try:
            self.engine = sqlalchemy.create_engine(engine_string)
            SessionInstance = sessionmaker(bind=self.engine)
            self.session: Session = SessionInstance()
        except sqlalchemy.exc.ArgumentError:
            logger.error("Could not parse engine URL from %s", engine_string)

    def close(self):
        """Closes session
        Returns: None
        """
        self.session.close()

    def get_latest(self, num_tiktoks) -> List[str]:
        """Fetch the most recent TikToks from connected db

        Args:
            num_tiktoks (`int`): Number of videos to return

        Returns:
            List: List of links
        """
        conn = self.engine.connect()

        links = conn.execute(
            f"""
        SELECT shortlink
        FROM tiktoks
        ORDER BY timestamp DESC
        LIMIT {num_tiktoks}"""
        ).all()
        logger.info("DB returned %i records", len(links))

        # Query returns each link as a 1-tuple, get rid of tuples
        links = [link[0] for link in links]
        return links

    def add_to_db(self, newlink: TikTok):
        """Add TikTok ORM object to db

        Args:
            newlink (TikTok): TikTok SQLAlchemy object
        """
        self.session.add(newlink)
        self.session.commit()
        logger.debug("Committed 1 record: %s", newlink.shortlink)
