import psycopg2
import os 

conn = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

cursor.execute(
    """ SELECT name, salary,
            (SELECT AVG(salary) FROM employees) as company_avg,
            salary - (SELECT AVG(salary) FROM employees) as diff_from_avg
        FROM employees
    """
)

data = cursor.fetchall()
print(data)


cursor.execute(
    """ 
    SELECT name, salary, dept 
    FROM employees
    WHERE salary > 
    (SELECT AVG(salary) from employees where dept = 'Finance')
    

"""
)

cursor.execute(
    """
    SELECT name, salary, dept FROM employees
	WHERE dept IN (
	SELECT dept FROM employees GROUP BY dept HAVING AVG(salary) > 60000
	)
"""
)
data = cursor.fetchall()
print(data)

# WHERE filters rows before grouping.
# The HAVING filters the data after the GROUP BY.

cursor.execute(
    """ 
        EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 70000
"""
)
data = cursor.fetchall()
print(data)

# Seq scan - this goes through every row one by one
# cost - this will tell the cost to run that particular query
# actual time - this will tell exact execution time 



# Even after using Index here Postgres still uses seq_scan because the data is very less in our table 
# and it is cost effective to use seq scan than index 


# Before index
cursor.execute("EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 70000")
print(cursor.fetchall())

# Create index
cursor.execute("CREATE INDEX IF NOT EXISTS idx_salary ON employees(salary)")
conn.commit()

# After index
cursor.execute("EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 70000")
print(cursor.fetchall())



