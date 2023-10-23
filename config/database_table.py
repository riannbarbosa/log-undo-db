from config import file
# Cria tabela no banco de dados criado
def create(cursor):
   print("Criando tabela...")
   cursor.execute('DROP TABLE IF EXISTS data_log')
   cursor.execute('''CREATE TABLE IF NOT EXISTS
           data_log(
           id SERIAL PRIMARY KEY,
           A INTEGER NOT NULL,
           B INTEGER NOT NULL
           );
           ''')
   print("Tabela criada com sucesso!")

def table_populate(cursor):
        print("Populando tabela...")
        try:
                data = file.file_metadata()
                for i in data:
                        if len(i) == 3:
                                cursor.execute(f'''INSERT INTO data_log (id, A, B)
                                VALUES ({i[0]}, {i[1]}, {i[2]});''')
                        else:   
                                cursor.execute(f'''INSERT INTO data_log (A, B)
                                VALUES ({i[0]}, {i[1]});''')
        except:
                print("Erro ao inserir dados na tabela")
                exit(1)
        finally:        
                 print("Tabela populada com sucesso!")
                 




       