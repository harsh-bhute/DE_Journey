import requests
import pandas as pd
import sqlite3


response = requests.get("https://jsonplaceholder.typicode.com/posts")

posts = response.json()
print(posts)

df = pd.DataFrame(posts)

print(df.shape)

print(df.iloc[:5, :])

df['body'] = df['body'].str.replace('\n','')

print(df.columns)



df['title_length'] = df['title'].str.split().str.len()
print(df)


df = df[df['title_length'] > 5]

df.rename(columns={'userId':'user_id'}, inplace= True)

df.reset_index(drop= True)

conn = sqlite3.connect('etl.db')

cursor = conn.cursor()

df.to_sql('User_data', conn, if_exists='replace',index = False)

print(pd.read_sql('SELECT * FROM User_data LIMIT 10', conn))