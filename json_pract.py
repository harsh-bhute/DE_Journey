import requests
import sqlite3

response = requests.get("https://jsonplaceholder.typicode.com/users")
user = response.json()
print(user[0])

# User.db data

conn = sqlite3.connect('users.db')

cursor = conn.cursor()

cursor.execute(""" 
    CREATE TABLE EMPLOYEE( ID INT,
               NAME TEXT,
               EMAIL TEXT,
               CITY TEXT
               )

""")
conn.commit()
print("Table created")

for i in user:
    cursor.execute("INSERT INTO EMPLOYEE VALUES(?,?,?,?)",
                   (i['id'],i['name'],i['email'],i['address']['city']))
conn.commit()

cursor.execute("SELECT * FROM EMPLOYEE")
OUTPUT = cursor.fetchall()
print(OUTPUT)
#-----------------------------------
print(user[0])

#Task 2 — Access nested data
for i in user:
    print(f"Name:{i['name']} | City :{i['address']['city']} | Company Name: {i['company']['name']}")


#Task 3 — Filter and extract

for i in user:
    if "son" in i["company"]["name"].lower():
        print(f"Name :{i['name']}  | Company name:{i["company"]["name"]}")



