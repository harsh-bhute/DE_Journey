import sqlite3

conn = sqlite3.connect("report.db")
cursor = conn.cursor()

# Creation of Table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS EMPLOYEES(
        ID INT,
        NAME TEXT,
        DEPT TEXT

    )
    """
)
conn.commit()
print("Table Created")

# Addition of Data to table

cursor.execute("INSERT INTO EMPLOYEES VALUES(1,'HARSH','IT')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(2,'KARAN','IT')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(3,'DEVESH','SALES')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(4,'NARESH','HR')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(5,'SHIVAM','IT')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(6,'PAWAN','HR')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(7,'NAVIN','SALES')")

conn.commit()
# getting all users 
cursor.execute("SELECT * FROM EMPLOYEES")
ROWS = cursor.fetchall()

for row in ROWS:
    print(f"ID:{row[0]} | Name:{row[1]} | Dept:{row[2]}")

# Function to get the employees by their Dept.
def get_employees_by_dept(dept):
    
    cursor.execute("SELECT * FROM EMPLOYEES WHERE DEPT = ?",(dept,))
    ROWS = cursor.fetchall()

    for row in ROWS:
        print(f"ID:{row[0]} | Name:{row[1]} | Dept:{row[2]}")


get_employees_by_dept('HR')

