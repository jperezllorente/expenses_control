import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient, UpdateOne
from src.mongo_functions import insert_object
from configuration.config import data
from src.mongo_functions import *
from src.categ_functions import *
from src.display_functions import *
from src.lists import categories_expenses, unique_categories, unique_subcategories, subcategories_expenses, cate_subcategories, fixed_costs_table
from src.visualization import category_plot, subcategory_plot
from keys.bank import *

st.title('Expenses control')

st.header('General Expenses')

gen_expenses = st.checkbox('Display Global Graph')
if gen_expenses:
    category_plot()


st.header('Subcategories')

option = st.selectbox(
     'What subcategory do you wish to display?',
     (unique_categories))

subcategories_count = subcategories_expenses(option)
subcategories_names = cate_subcategories(option)

subcat_expenses = st.checkbox('Display Subcategories Graph')
if subcat_expenses:
    subcategory_plot(subcategories_count, subcategories_names)

st.header('Fixed Costs')

st.table(fixed_costs_table)


