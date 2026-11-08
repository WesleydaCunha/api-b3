"""Insere alguns tickers e cryptos de EXEMPLO para validar os endpoints.

Uso (rodar a partir da raiz do projeto):

    python seed_sample.py

O destino é o mesmo do app: Turso se TURSO_DATABASE_URL/TURSO_AUTH_TOKEN
estiverem no .env (ou nas variáveis de ambiente), senão o SQLite local.

Pode ser rodado de novo sem duplicar (remove e reinsere os exemplos).
"""
from src.connections_db.get_data_local import connect as connect_tickers
from src.connections_db.connections_cryptocurrencies import ConnectionDBCryptoCurrencies

SAMPLE_STOCKS = [
    # ticker, nome, dy, preco_min, preco_max, dividendo, oscilacao, valor, site_ri, valorizacao, cnpj
    ("PETR4", "PETROBRAS PFD", 7.2, 34.5, 44.1, 1.85, 0.82, 42.33, "https://ri.petrobras.com.br", 12.5, "33.000.167/0001-01"),
    ("VALE3", "VALE ON", 5.8, 55.1, 72.4, 1.42, -0.34, 61.28, "https://www.vale.com", 8.1, "33.592.510/0001-54"),
    ("ITUB4", "ITAU UNIBANCO PN", 4.9, 36.8, 52.6, 0.68, 0.45, 50.12, "https://www.itau.com.br", 15.3, "60.872.504/0001-23"),
    ("WEGE3", "WEG ON", 1.2, 34.2, 46.9, 0.21, 0.12, 41.77, "https://www.weg.net", 9.4, "84.904.418/0001-42"),
    ("BOVA11", "BOVA11 ETF", 6.5, 120.4, 138.9, 1.05, 0.23, 130.55, "https://www.b3.com.br", 4.7, "none"),
    ("BBSE3", "BB SEGURIDADE ON", 8.4, 26.3, 35.8, 0.91, -0.18, 33.65, "https://www.bancodobrasil.com.br", 11.2, "08.016.890/0001-34"),
]

SAMPLE_CRYPTOS = [
    {
        "uuid": "Qwsogvtv82FCd",
        "symbol": "BTC",
        "name": "Bitcoin",
        "color": "#f7931a",
        "iconUrl": "https://cdn.coinranking.com/bOaIHsD/Bitcoin.svg",
        "marketCap": "1900000000000",
        "price": "94500",
        "change": "2.4",
        "rank": 1,
        "lowVolume": "42000000000",
        "coinrankingUrl": "https://coinranking.com/coin/Qwsogvtv82FCd-bitcoin-btc",
        "24hVolume": "42000000000",
        "btcPrice": "1",
    },
    {
        "uuid": "Qwsogvtv82FCd",
        "symbol": "ETH",
        "name": "Ethereum",
        "color": "#3c3c3d",
        "iconUrl": "https://cdn.coinranking.com/B1N19LfzF/Ethereum.svg",
        "marketCap": "410000000000",
        "price": "3400",
        "change": "1.7",
        "rank": 2,
        "lowVolume": "18000000000",
        "coinrankingUrl": "https://coinranking.com/coin/Qwsogvtv82FCd-ethereum-eth",
        "24hVolume": "18000000000",
        "btcPrice": "0.036",
    },
]

LOGO_PLACEHOLDER = "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
INFO_SAMPLE = "Dados de EXEMPLO para testes (não são cotações reais)"


def main():
    db = connect_tickers()
    tickers = [s[0] for s in SAMPLE_STOCKS]
    placeholders = ", ".join(f"'{t}'" for t in tickers)
    db.execute(f"DELETE FROM dataStock WHERE ticker IN ({placeholders})")
    for (ticker, nome, dy, pmin, pmax, div, oscil, valor, site_ri, valz, cnpj) in SAMPLE_STOCKS:
        db.execute(
            "INSERT INTO dataStock VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (nome, LOGO_PLACEHOLDER, INFO_SAMPLE, ticker, dy, pmin, pmax, div, oscil, valor, site_ri, valz, cnpj),
        )
    db.commit()
    db.close()

    crypto = ConnectionDBCryptoCurrencies()
    names = [c["name"] for c in SAMPLE_CRYPTOS]
    placeholders = ", ".join(f"'{n}'" for n in names)
    crypto.db.execute(f"DELETE FROM cryptos WHERE name IN ({placeholders})")
    crypto.db.commit()
    for coin in SAMPLE_CRYPTOS:
        crypto.addValues(coin)
    crypto.db.commit()
    crypto.db.close()

    print(f"OK: {len(SAMPLE_STOCKS)} tickers de exemplo e {len(SAMPLE_CRYPTOS)} cryptos gravados.")


if __name__ == "__main__":
    main()
