from pymongo import MongoClient
import pandas as pd
import os
from src.mongo_functions import collection_to_pd

DBURL ="mongodb://localhost/expenses_control"

#Vamos a conectar con la base de datos de mongo en local
if not (DBURL):
    raise ValueError("Tienes que especificar una URL pls")


client = MongoClient(DBURL)
db = client.get_database()
bank_mvts = db["movements"]
bank_cat = db['categories']
bank_subcat = db['subcategories']
test = db['test']

data = collection_to_pd(bank_mvts)

