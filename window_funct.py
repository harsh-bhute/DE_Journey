import psycopg2
import os 


conn = psycopg2.connect(
    host =os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)


cursor = conn.cursor()

cursor.execute("DELETE FROM employees")
cursor.execute(""" 
    INSERT INTO employees(name, dept, salary, joining_date) VALUES
    ('Aarav Sharma', 'IT', 65000, '2022-06-15'),
    ('Priya Mehta', 'HR', 52000, '2021-09-20'),
    ('Rahul Patil', 'Finance', 58000, '2023-01-10'),
    ('Sneha Joshi', 'IT', 72000, '2020-11-05'),
    ('Vikram Singh', 'Sales', 48000, '2022-03-18'),
    ('Neha Kulkarni', 'HR', 61000, '2023-07-12'),
    ('Rohan Deshmukh', 'Finance', 75000, '2019-08-25'),
    ('Ananya Rao', 'IT', 85000, '2021-04-30'),
    ('Kunal Verma', 'Sales', 55000, '2024-02-14'),
    ('Ishita Shah', 'Finance', 68000, '2022-10-08'),
    ('Amit Tiwari', 'IT', 91000, '2020-01-15'),
    ('Divya Nair', 'HR', 47000, '2024-05-01'),
    ('Saurabh Gupta', 'Sales', 63000, '2021-11-22'),
    ('Pooja Iyer', 'Finance', 82000, '2018-07-30'),
    ('Karan Malhotra', 'IT', 77000, '2023-09-10')
""")

conn.commit()

cursor.execute("SELECT name, salary, dept, ROW_NUMBER() OVER(PARTITION BY dept ORDER BY salary DESC) FROM employees")
result = cursor.fetchall()
print(result)

cursor.execute("INSERT INTO employees(name, dept,salary, joining_date) VALUES('Krishnan Iyyer','IT',77000,'2022-09-09')")
conn.commit()

cursor.execute("SELECT name, salary, dept, RANK() OVER(ORDER BY SALARY DESC) FROM employees")
result = cursor.fetchall()
print(result)

cursor.execute("SELECT name, salary, dept, DENSE_RANK() OVER(ORDER BY SALARY DESC) FROM employees")
result = cursor.fetchall()
print(result)

# In Rank we get the sequence ranked for each row and the duplicates are also considerd as separate but given the same rank,meaning the next rank will get the skipped rank.
# In Dense_Rank ,both the duplicates are given same rank but considerd same as well meaning the next rank will get the rank without skip

cursor.execute("""SELECT name, dept, salary,
    LAG(salary) OVER(PARTITION BY dept ORDER BY joining_date) as prev_salary,
    LEAD(salary) OVER(PARTITION BY dept ORDER BY joining_date) as next_salary
FROM employees""")
result = cursor.fetchall()
print(result)

# LAG() provides the previous value and the significance is we can compare it with the current one.
# LEAD() provides the next value and the significance is same.

cursor.execute(""" SELECT name,dept,salary,
	SUM(salary) OVER(PARTITION BY dept ORDER BY joining_date) as Total_department
FROM employees;""")
result = cursor.fetchall()
print(result)




