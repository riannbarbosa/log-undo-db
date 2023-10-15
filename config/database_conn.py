import os
from dotenv import load_dotenv, find_dotenv
import psycopg2

load_dotenv(find_dotenv())
def connect():
    conn = None
    try:

        # Se conecta ao banco de dados padrão
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        print(conn)
        cursor = conn.cursor()  
        cursor.execute('SELECT %s as connected;', ('Connection to postgres successful!',))    
        record = cursor.fetchone()
        print(record)
        cursor.close()
        return conn, cursor, record
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error connecting to PostgreSQL", error)

    finally:
        if conn is not None:
            conn.close()


    
