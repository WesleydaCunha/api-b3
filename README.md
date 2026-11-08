# API Ações
### API simples que retorna: Preço, DY, ultimo valor em dividendos, logo, preço mínimo em 12 meses, preço maxímo em 12 meses, oscilação diária, oscilação anual, cnpj e link do site de RI.

### Libs Utilizadas:
- Fast API
- numpy
- sqlite3
- beautifulSoup4

### Descrição do Funcionamento:
Ao executar: <code>python main.py</code>, Fast API irá executar localmente na porta 8000(no debug), abrindo as seguintes rotas: 
  - docs (rota padrão do Fast API)
  - get-tickers
  - get-ticker/{nome da ação. exemplo: petr4}
  - get-tickers-by-order/{exemplo: valor_cota}
  - get-values-cryptos

Ao executar: <code>python updateValues.py</code>, será feito web-scraping com bs4(Beautiful Soup) no site <a href="https://statusinvest.com.br">Status Invest</a>, onde irá atualizar os tickers(FIIs, BDRs, ETFs e Ações) e os valores das Crypto Moedas no site <a href="https://coinranking.com/">Coin Ranking</a>

Ao clocar o projeto, o dev deverá criar uma conta de desenvolvedor no site <a href="https://developers.coinranking.com/api">Coin Ranking Developers</a>, para gerar sua API de cotação das Crypto Moedas, e colocar no arquivo:

* get_price_cryptocurrencies.py

Substituindo API_KEY pela chave gerada anteriormente.

Projeto com deploy no <a href="https://heroku.com">Heroku</a>, na url: <a href="https://api-b3-python.herokuapp.com">https://api-b3-python.herokuapp.com</a>

<img src="https://img.shields.io/github/stars/ramonpaolo/api-b3" alt="Stars"/> <img src="https://img.shields.io/github/license/ramonpaolo/api-b3?color=2b9348" alt="License"/>
![GitHub repo size](https://img.shields.io/github/repo-size/ramonpaolo/api-b3) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask) ![GitHub top language](https://img.shields.io/github/languages/top/ramonpaolo/api-b3)

### Banco de dados (Turso)
O app usa SQLite local (`database/*.db`) quando `TURSO_DATABASE_URL` e `TURSO_AUTH_TOKEN` **não** estão definidas. Quando definidas, usa o [Turso](https://turso.tech/) (SQLite na nuvem, persistente) — recomendado para o deploy no Render, onde o disco local é temporário e os dados seriam perdidos a cada deploy.

```bash
# 1. Instale o Turso CLI (https://docs.turso.tech/quickstart)
# 2. Crie o banco e o token
turso db create api-b3 --tursodb
turso db tokens create api-b3
```

Depois configure em **Render → Settings → Environment** (e no `.env` local):
- `TURSO_DATABASE_URL` (ex.: `libsql://api-b3.seu-usuario.turso.io`)
- `TURSO_AUTH_TOKEN`

Veja o `.env.example` na raiz. As tabelas são criadas automaticamente pelo app (`CREATE TABLE IF NOT EXISTS`) quando o banco está vazio.

### Povoando os dados
```bash
cd src
python updateValues.py
```
Faz o scraping dos tickers (StatusInvest) e das cryptos (CoinRanking, exige `API_KEY`). Com as variáveis do Turso configuradas, os dados vão direto para o banco na nuvem.
