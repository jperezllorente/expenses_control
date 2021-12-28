from pymongo import MongoClient, UpdateOne
import pandas as pd
from datetime import datetime, timedelta
import glob, os, shutil
import time

def remove_docs(collection):
    return collection.remove({})

def collection_to_pd(collection):
    return pd.DataFrame(list(collection.find({},{'_id':0})))

def insert_object(df, collection):
    '''
    This function inserts all the information from the dataframe we created with the previous function as a Mongodb object.
    This object will have two field: title (name of the film or show) and reviews (array with all the reviews users have made)
    '''

    collection.insert_many(df.to_dict('records'))

def insert_single_object(collection):
    date = datetime.now().strftime("%d/%m/%Y")
    description = str(input('Describe the money flow briefly:'))
    quantity = float(input('Insert the correcto amount rounded to two decimal numbers:'))
    category = input('To what category does the movement belong?')
    return collection.insert_one({'date':date,
                            'description':description,
                            'quantity':quantity,
                            'category':category})