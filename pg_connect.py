import psycopg2

conn = psycopg2.connect(
    host ="localhost",
    database = "de_week3",
    user = "postgres",
    password = "2003"

)

cursor = conn.cursor()
print("Connected to PostgreSQL successfully")

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS employees(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        dept VARCHAR(100),
        salary INTEGER,
        joining_date DATE
    )
""")
conn.commit()

cursor.execute(""" 
    INSERT INTO employees(name,dept,salary,joining_date)
    VALUES
        ('Aarav Sharma', 'IT', 65000, '2022-06-15'),
        ('Priya Mehta', 'HR', 52000, '2021-09-20'),
        ('Rahul Patil', 'Finance', 58000, '2023-01-10'),
        ('Sneha Joshi', 'IT', 72000, '2020-11-05'),
        ('Vikram Singh', 'Sales', 48000, '2022-03-18'),
        ('Neha Kulkarni', 'HR', 61000, '2023-07-12'),
        ('Rohan Deshmukh', 'Finance', 75000, '2019-08-25'),
        ('Ananya Rao', 'IT', 85000, '2021-04-30'),
        ('Kunal Verma', 'Sales', 55000, '2024-02-14'),
        ('Ishita Shah', 'Finance', 68000, '2022-10-08')
""")
conn.commit()

cursor.execute("SELECT * FROM employees")
data = cursor.fetchall()
for row in data:
    print(row)

cursor.execute("SELECT * FROM employees where salary > 70000")
data = cursor.fetchall()
for row in data:
    print(row)

cursor.execute("SELECT dept ,COUNT(*) FROM employees GROUP BY dept")
data = cursor.fetchall()
for row in data:
    print(row)

# SQLite automatically generates the interger IDs for Interger Primary Key, while PostgreSQL SERIAL creates an associated ssequence.
# Postgres support length limited VARCHAR(100) sqlite also accepts but doesnt enforce it the same way.
#  Postgres requires connection info to a database server but SQLITE only needs a database file
# SQLITE  is mainly a local file, python program directly opens it , but in PostgreSQL a separate server manages the database.python program connects to that server and sends SQL cmds.