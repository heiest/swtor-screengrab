-- sqlite3 -init initialize_prices_db.sql prices.db

CREATE TABLE IF NOT EXISTS items(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS prices(
    item_id INTEGER NOT NULL,
    price BIGINT,
    time_stamp BIGINT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE INDEX IF NOT EXISTS price_index ON prices(price);
CREATE INDEX IF NOT EXISTS time_stamp_index ON prices(time_stamp);