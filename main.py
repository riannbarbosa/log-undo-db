from config.database_conn import create_db_connection
from config.database_table import create, table_populate
import psycopg2

def main():
    conn = None
    try:
        db_connection = create_db_connection()
        if(db_connection):
            print("Conectado ao banco de dados.")
            conn = db_connection
            cursor = conn.cursor()
            create(cursor)
            table_populate(cursor)
            cursor.close()
            conn.commit()
        else:
            print("Falha ao conectar ao banco de dados Postgre.")
            exit(1)

    except (Exception, psycopg2.DatabaseError) as error:
        print('Erro:', error)

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()