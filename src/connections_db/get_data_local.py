import os
import sqlite3

try:
    from src.connections_db.db import connect_db
except ImportError:
    from connections_db.db import connect_db

os.makedirs("database", exist_ok=True)

SCHEMA_DATA_STOCK = """
CREATE TABLE IF NOT EXISTS dataStock(
    nome text,
    logo text,
    info text,
    ticker text,
    dy number,
    precoMinimoCotaEmUmAno number,
    precoMaximoCotaEmUmAno number,
    dividendoEmUmAno number,
    oscilacaoCota number,
    valorCota number,
    linkSiteRi text,
    valorizacaoCotaUmAno number,
    cnpj text
);
"""


def connect():
    """Conecta no banco criando pasta e tabela se ainda não existirem."""
    db = connect_db("./database/tickers.db")
    db.execute(SCHEMA_DATA_STOCK)
    db.commit()
    return db


class DataLocal():
    def getData(self, ticker: str):
        db = connect()
        data = db.execute(f"select * from dataStock where ticker='{ticker.upper()}'").fetchall()
        db.close()
        if not data:
            return {"erro": f"Ticker '{ticker}' não encontrado"}
        # print(data[0])
        return {
            "nome": data[0][0],
            "logo": data[0][1],
            "info": data[0][2],
            "ticker": data[0][3],
            "dy": data[0][4],
            "preco_min_cota": data[0][5],
            "preco_max_cota": data[0][6],
            "ultimo_pagamento": data[0][7],
            "oscilacao_cota": data[0][8],
            "valor_cota": data[0][9],
            "linkSiteRi": data[0][10],
            "valorizacaoCota": data[0][11],
            "cnpj": data[0][12],
        }

    def getOrderDatas(self, order: str):
        db = connect()
        datas = db.execute(f"select * from dataStock order by {order}").fetchall()
        db.close()
        datasInJson = []
        for x in datas:
            if x[0] != "":
                datasInJson.append({"data": {
                    "nome": x[0],
                    "logo": x[1],
                    "info": x[2],
                    "ticker": x[3],
                    "dy": x[4],
                    "preco_min_cota": x[5],
                    "preco_max_cota": x[6],
                    "ultimo_pagamento": x[7],
                    "oscilacao_cota": x[8],
                    "valor_cota": x[9],
                    "linkSiteRi": x[10],
                    "valorizacaoCota": x[11],
                    "cnpj": x[12]}
                })
        return {"result": datasInJson}
