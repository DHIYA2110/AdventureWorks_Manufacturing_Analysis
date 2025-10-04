#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# --- Connection ---
conn = pyodbc.connect(
    'Driver={ODBC Driver 18 for SQL Server};'
    'Server=.\SQLEXPRESS;'
    'Database=AdventureWorks2019;'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)

# --- Load SQL and clean it ---
sql_file_path = r"C:\Users\pro\Downloads\AdventureWorks_Analysis\SQL Queries\Sick leave by job title.sql"
with open(sql_file_path, "r", encoding="utf-8") as f:
    query = f.read()

# Remove 'GO' and 'USE ...' lines
query = "\n".join([line for line in query.splitlines() 
                   if not line.strip().upper().startswith("GO") 
                   and not line.strip().upper().startswith("USE")])

# --- Run query ---
df = pd.read_sql_query(query, conn)
conn.close()

# Filter job titles with more than 5 employees
df = df[df['Num_Employees'] > 5]

# Identify technicians
df["Technician"] = df['Title'].str.startswith("Technician")

# --- Plot ---
plt.figure(figsize=(12,6))
plt.bar(df[df["Technician"]]['Title'], df[df["Technician"]]['Average_SickLeave'],
        color="tab:blue", label="Technicians")
plt.bar(df[~df["Technician"]]['Title'], df[~df["Technician"]]['Average_SickLeave'],
        color="tab:green", label="Other")
plt.axhline(y=45, linestyle='--', color='grey', label='Average Sickleave (45)')

# Annotate number of employees
for i in range(len(df)):
    height = df['Average_SickLeave'].iloc[i] / 2
    plt.text(df['Title'].iloc[i], height, df['Num_Employees'].iloc[i], 
             ha="center", va="bottom", color="red")

plt.xlabel('Job Title')
plt.ylabel('Average Sick Leave (hours)')
plt.title("Average Sick Leave by Job Title (Above 5 Employees)")
plt.legend(bbox_to_anchor=(0.4, 1.02))
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, ticks=range(len(df['Title'])), 
           labels=[title.replace(" Technician", "") for title in df['Title']])
plt.tight_layout()
plt.show()


# In[ ]:




