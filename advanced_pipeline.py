import psycopg2
import os
import logging

logging.basicConfig(
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s  - %(message)s'
)

try:
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )
except Exception as e:
    logging.info(f"Connection failed::",{e})

cursor = conn.cursor()

def Dept_report():
    try:
        cursor.execute(
            """
            WITH dept_stats AS (
                SELECT dept,
                    COUNT(*) as total_employees,
                    AVG(salary) as avg_salary,
                    MAX(salary) as highest,
                    MIN(salary) as lowest
                FROM employees
                GROUP BY dept
            ),
            above_avg AS (
                SELECT e.dept, COUNT(*) as above_avg_count
                FROM employees e
                JOIN dept_stats d ON e.dept = d.dept
                WHERE e.salary > d.avg_salary
                GROUP BY e.dept
            )
            SELECT d.dept, d.total_employees, d.avg_salary, d.highest, d.lowest, a.above_avg_count
            FROM dept_stats d
            JOIN above_avg a ON d.dept = a.dept
        """
        )
        
        data = cursor.fetchall()
        print(data)
        logging.info("Query ran successfully")
    except psycopg2.Error as e:
        logging.error(e)



def Company_Rank():
    try:
        cursor.execute(
            """
            SELECT name,
                dept,
                salary,
                RANK() OVER(PARTITION BY dept ORDER BY salary DESC) as Rank_dept,
                RANK() OVER(ORDER BY salary DESC) as Company_rank,
                
                NTILE(4) OVER(ORDER BY salary DESC)
                
            FROM employees
        """
        )
        logging.info("Query ran successfully")
        data = cursor.fetchall()
        print(data)
    except psycopg2.Error as e:
        logging.error(e)
   

def YOY_Joining_date():
    try:
        cursor.execute(
            """
            SELECT COUNT(name),
            EXTRACT(YEAR FROM joining_date) as year
            from employees
            GROUP BY year
            ORDER BY year
        """
        )
        logging.info("Query ran successfully")
        data = cursor.fetchall()
        print(data)
    except psycopg2.Error as e:
        logging.error(e)

    
def Salary_bands():
    try:
        cursor.execute(
            """
            SELECT name,salary,dept,
            CASE 
                WHEN salary <= 55000 THEN 'Junior'
                WHEN salary > 55000 AND salary <= 75000 THEN 'Mid'
                WHEN salary > 75000 THEN 'Senior'
            END as band
            FROM employees
            ORDER BY band, salary DESC
        """
        )
        logging.info("Query ran successfully")
        data = cursor.fetchall()
        print(data)
    except psycopg2.Error as e:
        logging.error(e)


def main():
    Dept_report()
    Company_Rank()
    YOY_Joining_date()
    Salary_bands()

if __name__ == "__main__":
    main()