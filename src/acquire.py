import logging
import json
from typing import List, Tuple

import sqlite3
from sqlite3 import Connection, Cursor
import yaml

logger = logging.getLogger(__name__)


def connect(uri: str) -> Tuple[Connection, Cursor]:
    """Establish connection to database

    Args:
        uri (`str`): SQLite path to db

    Returns:
        `sqlite3.Connection`, `sqlite3.Cursor`: Connection and cursor object
    """
    # Connect to db, generate cursor object
    connection = sqlite3.connect(uri)
    db_cursor = connection.cursor()
    logger.info("Connected to db at %s", uri)

    return connection, db_cursor


def get_past_tiktoks(cursor: Cursor, groupchat: str) -> List:
    """Extract messages pertaining to TikTok links from the
    Apple Messages database

    Args:
        cursor (`sqlite3.Cursor`): Cursor object for the SQLite database
        groupchat (`str`): Display name of the Messages conversation

    Returns:
        List: Return link and Cocoa Core timestamp for each message
        as a list of tuples
    """
    msglist = cursor.execute(
        f"""SELECT m.text, cmj.message_date
            FROM message AS m
            JOIN chat_message_join AS cmj ON m.ROWID=cmj.message_id
            JOIN chat AS c ON c.ROWID=cmj.chat_id
            WHERE c.display_name={groupchat}
            AND
            m.text LIKE "https://vm.tiktok.com%"
            ORDER BY cmj.message_date"""
    ).fetchall()
    logger.info(
        "Obtained %i records from db %s", len(msglist), cursor.connection
    )

    return msglist


def acquire(args):
    """Orchestration function to extract records from db"""
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config = config["acquire"]

    con, cur = connect(args.input)
    msglist = get_past_tiktoks(cur, config["groupchat"])

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(json.dumps(msglist))
            logger.info(
                "Generated JSON document with %i no of objects", len(msglist)
            )

    con.close()
