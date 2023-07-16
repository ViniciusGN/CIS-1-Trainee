import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import folium

df = pd.read_csv('Crime_Data_from_2020_to_Present.csv') #abrir o CSV
coluna_valores_unicos = df['Vict Sex'].unique()
print(coluna_valores_unicos)