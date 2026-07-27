import pandas as pd 
import requests

data = {
    "name":["Harsh","Rahul","Priya","Aman","Sneha"],
    "dept":["IT","Sales","IT","HR","Sales"],
    "salary":[50000,45000,60000,40000,55000]
}

df = pd.DataFrame(data)
print(df)
print(df.shape)
print(df.columns)

#Print only rows where dept == "IT"
print(df[df['dept'] == "IT"])

#Print only rows where salary > 50000
print(df[df['salary'] > 50000])

#Print IT employees earning more than 45000 — combine two conditions with &
print(df[(df["dept"] == "IT") & (df["salary"] > 45000)])

#Average salary across all employees
print(df["salary"].mean())

#Average salary per department
print(df.groupby("dept").mean("salary"))

#Who has the highest salary — print their name
print(df.loc[df["salary"].idxmax(),"name"])

#Load API data into Pandas 

response = requests.get("https://jsonplaceholder.typicode.com/users")

users = response.json()
print(users)
print(df.columns)

df = pd.DataFrame(users)

print(df)

print(df[["name","email","username"]])
u = 0
for i in df["username"]:
    if i[0] == "K":
        print(i)
        u = u+1
print(u)