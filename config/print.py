def new_line():
  print()

def print_update(transaction, old_value, log_values):
  row = log_values[0]
  column = log_values[1]
  new_value = log_values[2]

  print('TRANSAÇÃO '+ transaction +': No registro '+ row +', a coluna ' + column +' estava ' + str(old_value) + ' e no log atualizou para ' + new_value)


def print_transactions(committed_transactions):
  
  new_line()

  if not committed_transactions:
    print('Não houve nenhuma alteração no banco')
    return

  for transaction in committed_transactions:
      print('Transação '+ transaction +': realizou UNDO')


def print_json(cursor):
  id = []
  a = []
  b = []

  # Retorna todas as tuplas da tabela
  cursor.execute('SELECT * FROM data_log ORDER BY id')
  tuples = cursor.fetchall()

  for tuple in tuples:
    id.append(tuple[0])
    a.append(tuple[1])
    b.append(tuple[2])

  print('''
    {
      "INITIAL": {
        "id": '''+ str(id)[1:-1] +''',
        "A: '''+ str(a)[1:-1] +''',
        "B": '''+ str(b)[1:-1] +'''
      }
    }
  ''')
  