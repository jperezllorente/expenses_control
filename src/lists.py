from configuration.config import data, bank_cat, bank_subcat
import pandas as pd
from pymongo import MongoClient, UpdateOne


def unique_values(array):

    unique = []

    for number in range(0, len(array)):
        if array[number]['category'] not in unique:
            unique.append(array[number]['category'])
        else:
            pass

    return unique

def cate_subcategories(choice):

    return sorted(list(data[data.category == choice].subcategory.unique()))

def subcategories_expenses(choice):

    return data[data.category == choice].groupby('subcategory').agg({'quantity':'sum'}).abs().squeeze()

categories_expenses = data.groupby('category').agg({'quantity':'sum'}).abs().squeeze()

categories =list(bank_cat.find({},{'_id':0, 'category':1}))
subcategories =list(bank_subcat.find({},{'_id':0, 'category':1}))

unique_categories = sorted(unique_values(categories))
unique_subcategories = sorted(unique_values(subcategories))

subcategories_expenses('travel')

fixed_costs_desc = ['A MEDIUM CORPORATION', 'RECIB /CLUB DE PADEL Y TENIS F','CLUB DEPORTIVO JOSE VALEN','HBO Nordic AB']

fixed_costs_price = [4.23, 56.5, 67.0, 8.99]

fixed_costs_table = pd.DataFrame()

fixed_costs_table['description'] = fixed_costs_desc
fixed_costs_table['price'] = fixed_costs_price

fixed_costs_table.set_index('description', inplace = True)