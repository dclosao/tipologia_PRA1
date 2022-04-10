# importació de llibreries
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import csv
import re

# creem l'element del lloc web
page = requests.get("https://newluxbrand.com/shop/")

# creem l'objecte soup per a emmagatzemar el contingut de la pàgina
soup = BeautifulSoup(page.text, 'html.parser')


# creem llistes buides per a omplirles amb la iteració
# >df1
titles = []
prices = []
categories = []


# >df2
colors=[]
dimensions=[]
disponibilitats=[]
names=[]


for product_thum in soup.find_all('div', class_='astra-shop-thumbnail-wrap'):
    webs=product_thum.find('a', class_ ='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
    prod_web = requests.get(webs)
    prod_soup= BeautifulSoup(prod_web.text, 'html.parser')
    
    diponibilitat = prod_soup.find('div', class_='newlux_woo_single_product_stock').text
    disponibilitats.append(diponibilitat)
    
    name = prod_soup.find('h1', class_='product_title entry-title').text
    names.append(name)
    
    llista1=[]    
    for element in  prod_soup.select('.ficha_tecnica__param_name'):
        llista1.append(element.text)
    llista2=[]    
    for element in  prod_soup.select('.ficha_tecnica__param_value'):
        llista2.append(element.text)
    fitxa_final=zip(llista1,llista2)
    fitxa_final=list(fitxa_final)
    fitxa_final=dict(fitxa_final)
    if 'Color' in fitxa_final:
        color=fitxa_final['Color']
        colors.append(color)
    else:
        colors.append('')
    if 'Dimensiones del producto' in fitxa_final:
        dimension=fitxa_final['Dimensiones del producto']
        dimensions.append(dimension)
    else:
        dimensions.append('')


# iterem sobre l'objecte i obtenem els tres atributs que necessitem
for product in soup.find_all('div', class_='astra-shop-summary-wrap'):
    title = product.find('h2', class_="woocommerce-loop-product__title").text
    titles.append(title)
    price = product.span.span.bdi.text
    prices.append(price)
    category = product.find('span', class_="ast-woo-product-category").text
    categories.append(category)

# traiem els caracters als preus
prices = [n.replace('\xa0€', '') for n in prices]


# traiem els caracters als preus
prices = [n.replace('\xa0€', '') for n in prices]

# convertim les tres llistes en un dataframe
df1 = pd.DataFrame(np.column_stack([titles, prices, categories]), 
                               columns=['titles_l', 'prices', 'categories'])

df2 = pd.DataFrame(np.column_stack([names, disponibilitats, colors, dimensions]), 
                               columns=['titles_r', 'diponibilitats', 'colors','dimensions'])

# creem el dataframe final
df = df1.merge(df2, left_on='titles_l', right_on='titles_r')
# eliminem la columna duplicada
df.drop('titles_r', inplace=True, axis=1)
# canviem el nom de la columna title
df.rename(columns = {'titles_l': 'title'}, inplace=True)

# exportem en CSV
df.to_csv('output_scraping.csv', encoding='utf-8-sig', index=False)
