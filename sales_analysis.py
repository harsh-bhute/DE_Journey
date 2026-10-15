import pandas as pd
import psycopg2
import os
import logging
import requests
from sqlalchemy import create_engine

engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
logging.basicConfig(
    filename="SalesData.log",
    level= logging.INFO,
    format='%(asctime)s - %(levelname)s  - %(message)s'
)

conn = psycopg2.connect(
    host = os.getenv("DB_HOST"),
    database = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
    )
cursor = conn.cursor()

def load_data():
    df = pd.read_csv(r"C:\Users\HP\Downloads\sample_data.csv",encoding='latin1')
    logging.info("Converted to DF successfully.")
    logging.info(df.shape)
    logging.info(df.columns.tolist())
    logging.info(df.dtypes)
    logging.info(df.isnull().sum())
    df.drop(columns=['ADDRESSLINE2'], inplace=True)
    try:
        df.to_sql('sales_data',engine, if_exists='replace', index= False)
        logging.info("Data loaded to DB successfully.")
        cursor.execute(
            """
            SELECT COUNT(*) FROM sales_data
            """
        )
        count_rows = cursor.fetchall()
        logging.info(f"Total rows:{count_rows}")
    except ConnectionError as e:
        logging.error(e)
        conn.rollback()

def top_products():
    try:
        cursor.execute(
            """
            SELECT "PRODUCTLINE",SUM("QUANTITYORDERED") AS total_orders, SUM("SALES")AS total_revenue FROM sales_data 
            GROUP BY "PRODUCTLINE"
            ORDER BY total_revenue DESC
    """
        )
        logging.info("QUERY executed succcessfully")
        data = cursor.fetchall()
        logging.info(data)
    except psycopg2.Error as e:
        logging.error(e)


def monthly_trend():
    try:
        cursor.execute(
            """
            SELECT SUM("SALES"),"YEAR_ID" AS year,"MONTH_ID" as month FROM sales_data
            GROUP BY "YEAR_ID","MONTH_ID"
            ORDER BY year,month
        """
        )
        logging.info("Query Exceuted Successfully")
        data = cursor.fetchall()
        logging.info(data)
    except psycopg2.Error as e:
        logging.error(e)

def customer_segments():
    try:
        cursor.execute(
            """
        WITH customer_seg as (
            SELECT "CUSTOMERNAME" ,SUM("SALES") AS total_spend FROM sales_data
            GROUP BY "CUSTOMERNAME"
            )
            SELECT "CUSTOMERNAME",total_spend,
            CASE 
                WHEN total_spend > 100000 THEN 'High Value'
                WHEN total_spend >= 50000 AND total_spend < 100000 THEN 'Mid Value'
                WHEN total_spend < 50000 THEN 'Low Value'
            END AS segment_name
            FROM customer_seg        
        """
        )
        logging.info("Query Exceuted Successfully")
        data = cursor.fetchall()
        logging.info(data)
    except psycopg2.Error as e:
        logging.error(e)

def best_month_per_year():
    try:
        cursor.execute(
            """
            WITH best_month as (

            SELECT "YEAR_ID","MONTH_ID",SUM("SALES") as total_sales,
                RANK() OVER(PARTITION BY "YEAR_ID" ORDER BY SUM("SALES")DESC) AS rnk
                FROM sales_data
                GROUP BY "YEAR_ID","MONTH_ID"
            )
            SELECT "YEAR_ID","MONTH_ID",total_sales
            FROM best_month 
            WHERE rnk = 1    
                """
        )
        logging.info("Query Exceuted Successfully")
        data = cursor.fetchall()
        logging.info(data)
    except psycopg2.Error as e:
        logging.error(e)

def deal_size_analysis():
    try:
        cursor.execute(
            """
            SELECT "DEALSIZE",SUM("QUANTITYORDERED")AS count_of_orders,SUM("SALES") AS total_revenue,AVG("SALES") AS avg_revenue_per_deal
            FROM sales_data
            GROUP BY "DEALSIZE"
            ORDER BY SUM("SALES") DESC
        """
        )
        logging.info("Query Exceuted Successfully")
        data = cursor.fetchall()
        logging.info(data)
    except psycopg2.Error as e:
        logging.error(e)

def main():
    logging.info("Sales analysis pipline started")
    load_data()
    top_products()
    monthly_trend()
    customer_segments()
    best_month_per_year()
    deal_size_analysis()
    logging.info("Sales analysis pipeline ended.")

if __name__ == "__main__":
    main()