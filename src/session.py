import logging

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class SessionManager:
    def __init__(self, engine_string):
        """
        Args:
            engine_string: str - Engine string
        """
        try:
            self.engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except sqlalchemy.exc.ArgumentError:
            logger.error("Could not parse engine URL from %s", engine_string)

    def close(self):
        """Closes session
        Returns: None
        """
        self.session.close()

    def get_latest(self, num_tiktoks):
        conn = self.engine.connect()

        links = conn.execute(
            f"""
        SELECT shortlink
        FROM tiktoks
        ORDER BY timestamp DESC
        LIMIT {num_tiktoks}"""
        ).all()

        links = [link[0] for link in links]

        return links
