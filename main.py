from config.database_conn import connect
import psycopg2

def main():
    try:
        connect()   


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    main()