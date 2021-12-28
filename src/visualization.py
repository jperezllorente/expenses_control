import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
from configuration.config import data
from src.lists import categories_expenses, unique_categories



colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

def category_plot():

    fig1, ax1 = plt.subplots()

    ax1.pie(categories_expenses, labels = unique_categories, colors = colors, autopct='%1.1f%%', startangle=90,
           pctdistance=0.85)

    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.set_size_inches(9,9)
    fig.gca().add_artist(centre_circle)

    ax1.axis('equal')
    plt.tight_layout()
    st.pyplot(fig1)


def subcategory_plot(subcat_count, subcat_names):

    fig1, ax1 = plt.subplots()

    ax1.pie(subcat_count, labels = subcat_names, colors=colors, autopct='%1.1f%%', startangle=90,
            pctdistance=0.85)

    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.set_size_inches(9, 9)
    fig.gca().add_artist(centre_circle)

    ax1.axis('equal')
    plt.tight_layout()
    st.pyplot(fig1)



