import sqlite3
import logging

class SqliteDb:
    def __init__(self, logger = None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger.getChild(__name__)

        self.__connection = sqlite3.connect('prices.db')
        self.__connection.row_factory = sqlite3.Row

    def upsert_item(self, name):
        self.__connection.execute('INSERT OR IGNORE INTO items (name) values (?)', (name,))
        self.__connection.commit()
        return self.__connection.execute('SELECT id FROM items WHERE name = ?', (name,)).fetchone()[0]

    def insert_price(self, item_id, price, timestamp) -> None:
        self.__connection.execute('INSERT INTO prices VALUES (?, ?, ?);', (item_id, price, timestamp))
        self.__connection.commit()

    def get_prices_by_item_name(self, item_name):
        return self.__connection.execute('SELECT price, time_stamp FROM prices WHERE item_id = (SELECT id FROM items WHERE name = ?) ORDER BY time_stamp DESC;', (item_name,)).fetchall()

    def get_most_recent_price_timestamp(self, item_name):
        row = self.__connection.execute('SELECT time_stamp FROM prices WHERE item_id = (SELECT id FROM items WHERE name = ?) ORDER BY time_stamp DESC LIMIT 1', (item_name,)).fetchone()
        if row is not None:
            return row[0]

        return None