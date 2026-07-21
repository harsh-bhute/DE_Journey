import sqlite3

conn = sqlite3.connect("Company.db")
cursor = conn.cursor()

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

cursor.execute("INSERT INTO EMPLOYEES VALUES(1,'HARSH','IT')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(2,'KARAN','SALES')")
cursor.execute("INSERT INTO EMPLOYEES VALUES(3,'DEVESH','IT')")


cursor.execute("SELECT * FROM EMPLOYEES")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.commit()

cursor.execute("SELECT * FROM EMPLOYEES WHERE DEPT = 'IT'")
rows = cursor.fetchall()

for row in rows:
   print(f"ID:{row[0]} | NAME:{row[1]} | DEPT:{row[2]}")

conn.close()