import psycopg2
import os


conn = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM employees")
data = cursor.fetchall()
print(data)


# calculates average salary per department, then use it to find employees earning above their department average:
cursor.execute(""" 
    WITH dept_average AS(
        SELECT
            dept,
            AVG(salary) as Avg_sal
        FROM employees
        GROUP BY dept
    ) 
    SELECT e.name, e.dept, e.salary, d.Avg_sal
    FROM employees e
    JOIN dept_average d
    ON e.dept = d.dept
    WHERE e.salary > d.Avg_sal 
""")
data = cursor.fetchall()
print(data)

# first CTE: find the highest salary in each department
# Second CTE: find the lowest salary in each department
# Final query: show dept, highest, lowest, and the difference between them

cursor.execute(""" 
    WITH highest_sal AS(
        SELECT
            dept, 
            MAX(salary) as High
        FROM employees 
        GROUP BY dept    
    ),
    lowest_sal AS (
        SELECT dept,
            MIN(salary) as Low
        FROM employees
        GROUP BY dept
    )
    SELECT
    h.dept,
    h.High,
    l.low,
    (h.High - l.low) as difference
    FROM highest_sal h
    JOIN lowest_sal l
    ON h.dept = l.dept

""")
data = cursor.fetchall()
print(data)
#a CTE that ranks employees within their department by salary, then in the outer query filter to show only the top 2 earners per department.

cursor.execute(""" WITH Salary_Rank AS(
    SELECT
		name,
		dept,
		salary,
		RANK() 
        OVER(PARTITION BY dept ORDER BY SALARY DESC) AS RANKING
	FROM employees
)
SELECT * FROM Salary_Rank WHERE RANKING < 3

""")
data = cursor.fetchall()
print(data)

#Recursive CTE
# The recursive CTE are used to get mostly the hierarachial parts like manager of manager , subfolders of folders etc .

cursor.execute(
    """ 
    WITH RECURSIVE counter AS (
	SELECT 1 as n
	UNION ALL
	SELECT n+1 FROM counter WHERE n< 10
	
)
SELECT * FROM counter
"""
)


