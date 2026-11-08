import re
import sqlite3
import wikipedia
from deep_translator import GoogleTranslator

try:
    from src.connections_db.db import connect_db
except ImportError:
    from connections_db.db import connect_db

infoAction = {}
dataJson = {}


def _value_by_title(soup, title: str, default=None):
    """Retorna o <strong class=value> do bloco identificado pelo title."""
    box = soup.find("div", attrs={"title": title})
    if box is None:
        return default
    strong = box.find("strong", class_="value")
    return strong.text.strip() if strong is not None else default


def _nome_from_page(soup, ticker: str):
    """Nome da empresa a partir da página (div de logotipo ou <title>)."""
    m = re.search(r"Logotipo da empresa '([^']+)'", str(soup))
    if m:
        return m.group(1)
    if soup.title and soup.title.text:
        parts = soup.title.text.split(" - ")
        if len(parts) >= 2:
            return parts[-1].split(":")[0].strip()
    return ticker.upper()


def _extract_values(soup, with_dividends: bool = True):
    """Extrai os indicadores do bloco 'top-info' (mesmo template para ações,
    FIIs, ETFs e BDRs). Ausência de um bloco vira None (tratado em writeData)."""
    infoAction["valor_cota"] = _value_by_title(soup, "Valor atual do ativo")
    infoAction["preco_min_cota"] = _value_by_title(soup, "Valor mínimo das últimas 52 semanas")
    infoAction["preco_max_cota"] = _value_by_title(soup, "Valor máximo das últimas 52 semanas")
    infoAction["dy"] = (
        _value_by_title(soup, "Dividend Yield com base nos últimos 12 meses")
        if with_dividends else None
    )

    # Último pagamento de dividendos (soma dos proventos dos últimos 12 meses)
    last_div = soup.find(
        "div", attrs={"title": "Soma total de proventos distribuídos nos últimos 12 meses"})
    if last_div is not None and with_dividends:
        sub = last_div.find("span", class_="sub-value")
        infoAction["ultimo_pagamento"] = sub.text.strip() if sub is not None else None
    else:
        infoAction["ultimo_pagamento"] = None

    infoAction["valorizacaoCota"] = _value_by_title(
        soup, "Valorização no preço do ativo com base nos últimos 12 meses")

    # Variação diária: primeiro <b class=v-align-middle> da página
    daily = soup.find("b", class_="v-align-middle")
    infoAction["oscilacao_cota"] = daily.text.strip() if daily is not None else None

    infoAction["cnpj"] = "none"
    infoAction["linkSiteRi"] = "none"
    return infoAction


class BasicData():
    def __init__(self, soup, ticker: str):
        self.soup = soup
        self.ticker = ticker

    def getValuesLocal(self):
        return None

    def getInfoWikipedia(self):
        try:
            text = wikipedia.summary("Empresa: " + infoAction["nome"], 3)
            return GoogleTranslator(
                source="auto", target="pt").translate(text)
        except:
            #print("Não conseguiu pegar da Wikipédia/traduzir")
            return "Nada encontrado...."

    def getDatasInternet(self):
        infoAction["nome"] = _nome_from_page(self.soup, self.ticker)
        infoAction["logo"] = self.getImage()
        infoAction["info"] = self.getInfoWikipedia()
        infoAction["ticker"] = self.ticker.upper()

        return infoAction

    def getImage(self):
        #print(str(self.soup.find_all("div")[338]).split("(")[1].split(")")[0])
        if self.soup.find("div", title="Logotipo da empresa '"+infoAction["nome"].upper()+"'") != None:
            getImagee = self.soup.find("div", title="Logotipo da empresa '"+infoAction["nome"].upper()+"'")
            print(f"Site da image: {getImagee} do ticker: {self.ticker} com o nome: {infoAction['nome']}")
            return "https://statusinvest.com.br" +getImagee.__str__().split("(")[1].split(")")[0]
        #elif str(self.soup.find_all("div")[338]).split("(")[1].split(")")[0] != None:
            #return "https://statusinvest.com.br" + str(self.soup.find_all("div")[338]).split("(")[1].split(")")[0]
        else:
            for x in self.soup.find_all("div"):
                if str(x).__contains__("data-img"):
                    try:
                        print(str(x).split("(")[1].split(")")[0])
                        return "https://statusinvest.com.br" + str(x).split("(")[1].split(")")[0]
                    except:
                        return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"
            return "https://ik.imagekit.io/9t3dbkxrtl/image_not_work_bkTPWw2iO.png"

    def getTagAlong(self):
        self.tagAlong = self.soup.find_all("strong", attrs={"class": "value"})[6].text
        return self.tagAlong

    def getLiquidezDiaria(self):
        self.liquidezMediaDiaria = self.soup.find_all("strong", attrs={"class": "value"})[7].text
        return self.liquidezMediaDiaria


    def writeData(self, infoAction):
        db = connect_db("./database/tickers.db")
        try:
            infoAction["dy"] = float(str(infoAction["dy"]).replace(",", "."))
        except:
            infoAction["dy"] = 0.0

        try:
            infoAction["valorizacaoCota"] = float(str(infoAction["valorizacaoCota"]).replace(",", ".").replace("%", ""))
        except:
            infoAction["valorizacaoCota"] = 0.0

        try:
            infoAction['preco_min_cota'] = float(str(infoAction["preco_min_cota"]).replace(",", ".").replace("R$ ", ""))
            infoAction['preco_max_cota'] = float(str(infoAction["preco_max_cota"]).replace(",", ".").replace("R$ ", ""))

        except:
            infoAction["preco_min_cota"] = 0.0
            infoAction["preco_max_cota"] = 0.0

        try:
            infoAction['ultimo_pagamento'] = float(str(infoAction["ultimo_pagamento"]).replace("R$ ", "").replace(".", "").replace(",", "."))
        except:
            infoAction['ultimo_pagamento'] = 0.0

        try:
            infoAction['oscilacao_cota'] = float(str(infoAction["oscilacao_cota"]).replace(",", ".").replace("%", ""))
        except:
            infoAction['oscilacao_cota'] = 0.0

        try:
            infoAction['valor_cota'] = float(str(infoAction["valor_cota"]).replace("R$ ", "").replace(".", "").replace(",", "."))
        except:
            infoAction['valor_cota'] = 0.0

        if len(db.execute(f"select * from dataStock where ticker='{self.ticker}'").fetchall()) >= 1:
            db.execute(f"update dataStock SET dy={infoAction['dy']}, precoMinimoCotaEmUmAno={infoAction['preco_min_cota']}, precoMaximoCotaEmUmAno={infoAction['preco_max_cota']}, dividendoEmUmAno={infoAction['ultimo_pagamento']}, oscilacaoCota={infoAction['oscilacao_cota']}, valorCota={infoAction['valor_cota']}, logo='{infoAction['logo']}', cnpj='{infoAction['cnpj']}', linkSiteRi='{infoAction['linkSiteRi']}', valorizacaoCotaUmAno={infoAction['valorizacaoCota']} where ticker='{infoAction['ticker']}'")
            #print("Ação atualizada")
        else:
            db.execute(f"insert into dataStock values('{infoAction['nome']}','{infoAction['logo']}','Nada sobre....','{infoAction['ticker']}',{infoAction['dy']},{infoAction['preco_min_cota']},{infoAction['preco_max_cota']}, {infoAction['ultimo_pagamento']}, {infoAction['oscilacao_cota']},{infoAction['valor_cota']}, '{infoAction['linkSiteRi']}', {infoAction['valorizacaoCota']}, '{infoAction['cnpj']}');")
            #print("Ação inserida")
        db.commit()
        return infoAction

#------------------------------------------
# Extratores por categoria (mesmo bloco 'top-info' do StatusInvest)

def getValuesMoneyBdrs(soup):
    return _extract_values(soup)

def getAllValuesBdrs(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyBdrs(soup)
    comandBasics.writeData(infoAction)
    return infoAction

#----------------------------------------

def getValuesMoneyEtfs(soup):
    return _extract_values(soup, with_dividends=False)

def getAllValuesEtfs(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyEtfs(soup)
    comandBasics.writeData(infoAction)
    return infoAction

#-----------------------

def getValuesMoneyStocks(soup):
    return _extract_values(soup)

def getAllValuesStocks(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyStocks(soup)
    comandBasics.writeData(infoAction)
    return infoAction

#-----------------------

def getValuesMoneyFiis(soup):
    return _extract_values(soup)

def getAllValuesFiis(soup, ticker: str):
    comandBasics = BasicData(soup, ticker)
    comandBasics.getDatasInternet()
    infoAction = getValuesMoneyFiis(soup)
    comandBasics.writeData(infoAction)
    return infoAction
