import requests
from bs4 import BeautifulSoup
import re

url_btc = 'https://coinmarketcap.com/currencies/bitcoin/'
url_xlm = 'https://coinmarketcap.com/currencies/stellar/'
url_xrp = 'https://coinmarketcap.com/currencies/xrp/'
url_gld = 'https://www.kitco.com/gold-price-today-usa/'
url_usd = 'https://transferwise.com/pl/currency-converter/usd-to-pln-rate'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

def check_price_usd(usd_to_pln):
    soup = get_url(url_usd)
    price_usd = soup.find(class_='text-success').get_text()
    price_usd = price_usd.replace(',','.')
    converted_price_usd = float(price_usd)
    converted_price_usd = round(usd_to_pln*converted_price_usd,3)
    return converted_price_usd

def get_url(url):
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def check_name_btc():
    soup = get_url(url_btc)
    name_btc = soup.find(class_='cmc-details-panel-header sc-1extin6-0 gMbCkP').get_text()
    name_btc = name_btc[1:8]
    return name_btc

def check_price_btc():
    soup = get_url(url_btc)
    price_btc = soup.find(class_='cmc-details-panel-price__price').get_text()
    price_btc = price_btc.replace(',','')
    converted_price_btc = float(price_btc[1:])
    converted_price_btc = round(converted_price_btc,3)
    return converted_price_btc

def check_name_xrp():
    soup = get_url(url_xrp)
    name_xrp = soup.find(class_='cmc-details-panel-header sc-1extin6-0 gMbCkP').get_text()
    name_xrp = name_xrp[1:4]
    return name_xrp

def check_price_xrp():
    soup = get_url(url_xrp)
    price_xrp = soup.find(class_='cmc-details-panel-price__price').get_text()
    price_xrp = price_xrp.replace(',','')
    converted_price_xrp = float(price_xrp[1:])
    converted_price_xrp = round(converted_price_xrp,3)
    return converted_price_xrp

def check_name_xlm():
    soup = get_url(url_xlm)
    name_xlm = soup.find(class_='cmc-details-panel-header sc-1extin6-0 gMbCkP').get_text()
    name_xlm = name_xlm[1:8]
    return name_xlm

def check_price_xlm():
    soup = get_url(url_xlm)
    price_xlm = soup.find(class_='cmc-details-panel-price__price').get_text()
    price_xlm = price_xlm.replace(',','')
    converted_price_xlm = float(price_xlm[1:])
    converted_price_xlm = round(converted_price_xlm,3)
    return converted_price_xlm

def check_name_gld():
    soup = get_url(url_gld)
    name_gld = soup.find(class_='table-price--header').get_text()
    name_gld = name_gld[2:6]
    return name_gld

def check_price_gld():
    soup = get_url(url_gld)
    price_gld = soup.find(class_='table-price--body-table--overview-bid').get_text()
    price_gld = price_gld[5:13].replace(',', '')
    converted_price_gld = float(price_gld[:])
    converted_price_gld = round(converted_price_gld,3)
    return converted_price_gld

def my_coin_value_usd(quantity,price_usd):
    coin_value_usd = quantity*price_usd
    coin_value_usd = round(coin_value_usd,3)
    return coin_value_usd

def my_coin_value_pln(quantity,price_pln):
    coin_value_pln = quantity*price_pln
    coin_value_pln = round(coin_value_pln,3)
    return coin_value_pln

def round_quantity(quantity):
    if (type(quantity) == float):
        quantity = round(quantity,3)
    elif (type(quantity) == int):
        quantity = round(float(quantity),1)
    return quantity
