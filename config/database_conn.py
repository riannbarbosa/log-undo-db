from decouple import config
import psycopg2

def create_db_connection():
          # Se conecta ao banco de dados padrão
    db_configurations = {
         "host": config('DB_HOST'),
         "dbname": config('DB_NAME'),
         "user": config('DB_USER'),
        "password": config('DB_PASSWORD')
    }
    print(db_configurations)

    try:
        connection = psycopg2.connect(**db_configurations)
        return connection

    
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados PostgreSQL: {e}")
        return None

if __name__ == "__main__":
    db_connection = create_db_connection()
    if db_connection:
        print("Conectado ao banco de dados.")
    else:
        print("Falha ao conectar ao banco de dados.")
