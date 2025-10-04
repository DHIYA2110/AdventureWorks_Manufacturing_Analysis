#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Connection ---
conn = pyodbc.connect(
    'Driver={ODBC Driver 18 for SQL Server};'
    'Server=.\SQLEXPRESS;'
    'Database=AdventureWorks2019;'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)

# --- Load SQL from file ---
sql_file = r"C:\Users\pro\Downloads\AdventureWorks_Analysis\SQL Queries\SALES BY COUNTRY NAME.sql"
with open(sql_file, "r", encoding="utf-8") as f:
    query = f.read()

# --- Run query into DataFrame ---
df = pd.read_sql_query(query, conn)
conn.close()

print(df.head())  # confirm query output

# --- Plot: Stacked horizontal bar chart ---
Y_axis = np.arange(len(df['CountryName']))

plt.figure(figsize=(10, 6))
plt.barh(df['CountryName'], df['Sales_LastYear'],
         label='Last Year', color='steelblue')
plt.barh(df['CountryName'], df['Sales_YTD'],
         left=df['Sales_LastYear'], label='Year To Date', color='mediumseagreen')

plt.xticks(
    ticks=[0, 10_000_000, 20_000_000, 30_000_000, 40_000_000, 50_000_000],
    labels=["0M", "$10M", "$20M", "$30M", "$40M", "$50M"]
)
plt.yticks(Y_axis, df['CountryName'])
plt.xlabel("Sales")
plt.ylabel("Country")
plt.title("Sales by Country")
plt.legend()
plt.tight_layout()
plt.grid(axis="x", linestyle='--', linewidth=0.5)
plt.gca().invert_yaxis()
plt.show()


# In[ ]:




