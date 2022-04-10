# tipologia_PRA1

Extrau els preus, la disponibilitat i certs atributs de la pàgina https://newluxbrand.com/shop/ 

Per a executar el codi deuen instal·lar-se les següents llibreries:
	
from bs4 import BeautifulSoup

import requests

import numpy as np

import pandas as pd

import csv

import re

El script s'ha d'executar amb el següent comando:
python tipologia_PRA1.py

Aquest script generarà un fitxer en format CSV amb les següents columnes: 

title

prices

categories

diponibilitats

colors

dimensions
