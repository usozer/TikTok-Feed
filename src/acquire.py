import logging

import sqlite3
from sqlite3 import Cursor
import yaml

logger = logging.getLogger(__name__)

def connect(uri: str):
    connection = sqlite3.connect(uri)
    db_cursor = connection.cursor()

    return connection, db_cursor


def get_past_tiktoks(cursor: Cursor, groupchat: str):
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

    return msglist


def acquire(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    config = config["acquire"]

    con, cur = connect(args.input)
    msglist = get_past_tiktoks(cur, config["groupchat"])

    if args.output is not None:
        with open(args.output, "w") as f:
            
            for record in msglist:
                f.write(str(record) + "\n")

    con.close()
