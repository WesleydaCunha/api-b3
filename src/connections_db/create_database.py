"""Cria (se ainda não existirem) os bancos SQLite em ./database.

Uso: python -m src.connections_db.create_database
"""
import os

os.makedirs("database", exist_ok=True)

from src.connections_db.get_data_local import connect as connect_tickers
from src.connections_db.connections_cryptocurrencies import ConnectionDBCryptoCurrencies

connect_tickers().close()
ConnectionDBCryptoCurrencies().db.close()

print("Bancos criados em ./database (tickers.db e cryptos.db)")
