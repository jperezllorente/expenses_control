from keys.bank import *
from src.mongo_functions import insert_object
from pymongo import MongoClient, UpdateOne
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import streamlit as st
from keys.bank import PASSWORD, USERNAME
from configuration.config import bank_mvts

def data_extraction():
    os.environ['WDM_LOG_LEVEL'] = '0'
    browser = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(browser, 10)
    browser.maximize_window()
    browser.get("https://bancaonline.bankinter.com/gestion/login.xhtml")
    browser.implicitly_wait(5)
    browser.find_element_by_xpath("//a[contains(text(),'aceptar')]").click()

    username = browser.find_element_by_name("uid")
    password = browser.find_element_by_name("password")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    browser.find_element_by_id("btEntrar").click()
    browser.implicitly_wait(5)

    charges = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '/html/body/main/div/div/section/div[1]/form[1]/section/div/div[7]/div[1]/div[2]/div[3]/ul/li[1]')))
    charges.click()

    download_charges_excel = wait.until(
        ec.element_to_be_clickable((By.XPATH, '//html/body/main/section/form/div[1]/span[4]/div/ul/li[1]/a')))
    download_charges_excel.click()

    return_home = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="menuCabecera"]/li[1]/a')))
    return_home.click()

    incomes = wait.until(ec.element_to_be_clickable(
        (By.XPATH, '/html/body/main/div/div/section/div[1]/form[1]/section/div/div[1]/div[1]/div[2]/div[3]/ul/li[1]')))
    incomes.click()

    download_incomes_excel = wait.until(
        ec.element_to_be_clickable((By.XPATH, '/html/body/main/section/div[1]/span[1]/div[1]/form/ul/li[1]/a')))
    download_incomes_excel.click()

    time.sleep(5)

    browser.close()


def move_file():
    incomes_file = 'C:\\Users\\juanp\\Downloads\\movimientos.xls'
    charges_file = 'C:\\Users\\juanp\\Downloads\\Movimientos (1).xls'
    destination = 'C:\\Users\\juanp\\proyectos_varios\\expenses_control\\data'

    try:
        shutil.move(charges_file, destination)
        shutil.move(incomes_file, destination)
    except:
        pass
    try:
        os.replace(charges_file, destination)
        os.replace(incomes_file, destination)
    except:
        pass



def data_insert(path_charges, path_incomes, collection):
    incomes = pd.read_excel(path_incomes)[3:]
    incomes.drop(['Unnamed: 1', 'Unnamed: 4'], axis=1, inplace=True)
    incomes.rename(columns={'IBAN: ES6701280067740100026987': 'date', 'Unnamed: 2': 'description',
                            'Unnamed: 3': 'quantity'}, inplace=True)

    charges = pd.read_excel(path_charges)
    list_index = charges.index[charges["Número de tarjeta: Visa Clasi (....2133)"] == 'Total Crédito'].tolist()
    for number in list_index:
        limit_index = number
    charges = charges[5:limit_index]
    charges.drop(['Unnamed: 2'], axis=1, inplace=True)
    charges.rename(columns={'Número de tarjeta: Visa Clasi (....2133)': 'date', 'Unnamed: 1': 'description',
                            'Unnamed: 3': 'quantity'}, inplace=True)
    charges['date'] = charges['date'].apply(lambda x: x.strftime('%d/%m/%Y'))

    complete = pd.concat([incomes, charges])

    current_month = datetime.today().date().replace(day=1).strftime('%m/%Y')
    first_day_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
    complete.drop(complete[complete.description == 'RECIBO VISA CLASICA'].index, inplace=True)

    old = pd.DataFrame(list(bank_mvts.find({'date': {'$regex': current_month}}, {'_id': 0, 'category': 0})))

    complete_up = complete.loc[complete['date'].str.contains(current_month)]
    final_df = pd.concat([old, complete_up])
    final_df.drop_duplicates(keep=False, inplace=True)
    final_df['category'] = list(map(categorization, final_df['description']))
    final_df['subcategory'] = list(map(subcategorization, final_df['description']))
    os.remove('data\\movimientos.xls')
    os.remove('data\\Movimientos (1).xls')

    option = st.text_input('What action do you want to take?')

    if option == 'insert':
        insert_object(complete, test)
        return 'Data succesfully inserted'

    elif option == 'update':
        if len(final_df) == 0:
            return 'Nothing to update'
        else:
            insert_object(final_df, test)
            ##insert_object(final_df, move)
            return 'Data succesfully updated'




def my_bank_movements():
    try:

        data_extraction()

    except:

        return st.text('There has been a problem with the conexion. Please, try again later')

    move_file()

    return data_insert('data\\movimientos.xls', 'data\\Movimientos (1).xls', test)

