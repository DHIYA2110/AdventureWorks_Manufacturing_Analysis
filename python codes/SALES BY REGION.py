#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyodbc 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Connection ---
conn = pyodbc.connect(
    'Driver={ODBC Driver 18 for SQL Server};'
    'Server=.\SQLEXPRESS;'
    'Database=AdventureWorks2019;'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)

# --- Load SQL from file ---
sql_file = r"C:\Users\pro\Downloads\AdventureWorks_Analysis\SQL Queries\SALES BY REGION.sql"
with open(sql_file, "r", encoding="utf-8") as f:
    query = f.read()

print(query)  # Optional: to confirm query

# --- Run query into DataFrame ---
df = pd.read_sql_query(query, conn)
conn.close()
print(df.head())

# --- Stacked bar chart for Sales by US Region ---
X_axis = np.arange(len(df['RegionName']))
plt.figure(figsize=(10,6))
plt.bar(X_axis - 0.2, df['Sales_YTD'], 0.4, label='Year To Date', color='mediumseagreen')
plt.bar(X_axis + 0.2, df['Sales_LastYear'], 0.4, label='Last Year', color='steelblue')
plt.xticks(X_axis, df['RegionName'])
plt.yticks(
    ticks=[0,2_000_000,4_000_000,6_000_000,8_000_000,10_000_000,12_000_000],
    labels=["$0M","$2M","$4M","$6M","$8M","$10M","$12M"]
)
plt.xlabel("Region")
plt.ylabel("Sales")
plt.title("Sales by Region in USA")
plt.grid(axis="y", linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# --- Pie charts ---
plt.figure(figsize=(12,6))

# Pie chart of Year-to-Date Sales
plt.subplot(1, 2, 1)
plt.pie(df['Sales_YTD'], autopct='%1.1f%%', pctdistance=0.7, labels=df['RegionName'])
plt.title("Year to Date")
plt.text(-1, -1.4, f"Total = ${round(df['Sales_YTD'].sum()/1_000_000,1)}M",
         fontsize="large", style='oblique')

# Pie chart of Last Year Sales
plt.subplot(1, 2, 2)
plt.pie(df['Sales_LastYear'], autopct='%1.1f%%', pctdistance=0.7, labels=df['RegionName'])
plt.title("Last Year")
plt.text(-1, -1.4, f"Total = ${round(df['Sales_LastYear'].sum()/1_000_000,1)}M",
         fontsize="large", style='oblique')

plt.suptitle('Sales by Region in USA')
plt.tight_layout()
plt.show()


# In[ ]:




