import requests
import pandas as pd
import sqlite3

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try :
    logging.info("Pipeline started")
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    response.raise_for_status()
    posts = response.json()

    df = pd.DataFrame(posts)

    print(df.shape)

    print(df.iloc[:5, :])

    df['body'] = df['body'].str.replace('\n','')

    print(df.columns)

    df['title_length'] = df['title'].str.split().str.len()


    df = df[df['title_length'] > 5]

    df.rename(columns={'userId':'user_id'}, inplace= True)

    df.reset_index(drop= True, inplace= True)

    conn = sqlite3.connect('etl.db')

    df.to_sql('User_data', conn, if_exists='replace',index = False)

    print(pd.read_sql('SELECT * FROM User_data LIMIT 10', conn))

except requests.exceptions.RequestException as e:
    #print(f"HTTP error: {e}")
    logging.exception("API call failed")
except sqlite3.Error as e:
    #print(f"THE db connection error:{e}")
    logging.exception("Error in db")
finally :
    try:
        conn.close()
    except:
        pass
    logging.info("The db connection has been closed")






