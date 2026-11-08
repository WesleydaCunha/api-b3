import os
import sqlite3

try:
    from src.connections_db.db import connect_db
except ImportError:
    from connections_db.db import connect_db

os.makedirs("database", exist_ok=True)

SCHEMA_CRYPTOS = """
CREATE TABLE IF NOT EXISTS cryptos(
    uuid text,
    symbol text,
    name text,
    color text,
    iconUrl text,
    marketCap number,
    price number,
    change number,
    rank number,
    lowVolume number,
    coinrankingUrl text,
    volume number,
    btcPrice number
);
"""


class ConnectionDBCryptoCurrencies():
    def __init__(self):
        self.db = connect_db("database/cryptos.db")
        self.db.execute(SCHEMA_CRYPTOS)
        self.db.commit()

    def createTable(self):
        self.db.execute(SCHEMA_CRYPTOS)
        self.db.commit()

    def updateValues(self, x: object):
        self.db.execute(f"update cryptos set marketCap={float(x['marketCap'])}, price={float(x['price'])}, change={float(x['change'])}, rank={x['rank']}, lowVolume={float(x['lowVolume'])}, volume={float(x['24hVolume'])}, btcPrice={float(x['btcPrice'])} where name='{x['name']}';")

    def addValues(self, x: object):
        self.db.execute(f"""insert into cryptos values('{x['uuid']}','{x['symbol']}','{x['name']}', '{x['color']}','{x['iconUrl']}', {float(x['marketCap'])} , {float(x['price'])}, {float(x['change'])}, {x['rank']}, {float(x['lowVolume'])},'{x['coinrankingUrl']}', {float(x['24hVolume'])},{float(x['btcPrice'])});""")

    def getValues(self):
        return self.db.execute("select * from cryptos;")
