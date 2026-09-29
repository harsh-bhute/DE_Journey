import sqlite3
import pandas as pd
import numpy as np

data = {
    "id": [1, 2, 3, 4, 5, 5, 6],
    "name": ["Harsh", "rahul", "PRIYA", "Aman", None, "Sneha", "sneha"],
    "dept": ["IT", "Sales", "IT", "HR", "Sales", None, "Sales"],
    "salary": [50000, 45000, None, 40000, 55000, 55000, 45000],
    "joining_date": ["2021-01-15", "2020-03-22", "2019-07-01", "2022-11-10", "2021-05-30", "2021-05-30", "2023-01-01"]
}

df = pd.DataFrame(data)
print(df)

#Problems 
# 1. the id are dupicate
# 2. the names are not in a consistent Camelcase
# 3. the dept has a none Value
# 4. the salary has NAN value in it 
# 5. there is None value in name 

#ID 
print(df["id"].isnull().sum())

#NAME
print(df["name"].isnull().sum())

#dept
print(df["dept"].isnull().sum())

#salary
print(df["salary"].isnull().sum())

#joining date
print(df["joining_date"].isnull().sum())

df['salary'] = df['salary'].fillna(df['salary'].mean().__round__(2))

df = df.dropna(subset='name')

print(df)

print(df.duplicated())
print(f"Rows before dedup: {len(df)}")
df = df.drop_duplicates()
print(f"Rows after dedup: {len(df)}")
# there are no duplicate rows

df['name'] = df['name'].str.title()


print(df["Joining_Year"].dtype)

df["joining_date"] = pd.to_datetime(df["joining_date"])

df["Joining_Year"] = df['joining_date'].dt.year

print(df)
print(df.info())
print(df.describe())



conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS clean_employees (
    id int,
    name TEXT,
    dept TEXT,
    salary REAL,
    joining_date DATE,
    Joining_Year INT)
      """)
conn.commit()

print(df)

for _, row in df.iterrows():
    cursor.execute(""" INSERT INTO clean_employees VALUES(?,?,?,?,?,?)""",
                   (row['id'],row['name'],row['dept'],row['salary'],row['joining_date'].strftime("%Y-%m-%d"),row['Joining_Year']))

conn.commit()
conn.close()

