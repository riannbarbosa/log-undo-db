import re
from file_read_backwards import FileReadBackwards
from config.print import print_transactions, print_json, print_update
def find_by_last_checkpoint_find(file):
  with FileReadBackwards(file, encoding='utf-8') as file:
      for line in file:
        matches = re.findall('<END CKPT>', line)
        if(matches):
           return matches[0].split(',')
  return []



def find_commited_trans(file, checkpoint_transactions):
    commited_trans = []
    print(checkpoint_transactions)
    with FileReadBackwards(file, encoding='utf-8') as file:
       for line in file:
          if 'CKPT' in line:    
             break
          matches = re.search(r'<commit (.+?)>', line)
          if(not matches):
             matches_start = re.search(r'<start (.+?)>', line)
             transaction = matches_start.group(1)
             commited_trans.append(transaction)
    return commited_trans          
            
def undo_changes(file_path, cursor, logged_transactions):
     with FileReadBackwards(file_path, encoding='utf-8') as file:
        for transaction in logged_transactions:
            print(logged_transactions)
            undoing = False
            for line in file:
                if f'<start {transaction}>' in line:
                    undoing = True
                    continue
                if undoing:
                    matches = re.search(rf'<{transaction},(.+?)>', line)
                    if matches:
                        values = matches.group(1).split(',')
                        cursor.execute(f'SELECT {values[1]} FROM data WHERE id = {values[0]}')
                        old_value = cursor.fetchone()[0]

                        if int(values[3]) != old_value:
                            cursor.execute(f'UPDATE data SET {values[1]} = {str(old_value)} WHERE id = {values[0]}')
                            print_update(transaction, old_value, values)
                    elif f'<commit {transaction}>' in line:
                        break
    

def read_log(cursor):
    file= 'files/input_log'
    try:
        checkpoint_trans = find_by_last_checkpoint_find(file)
        logged_transactions = find_commited_trans(file, checkpoint_trans)
        undo_changes(file, cursor, logged_transactions)

        print_transactions(checkpoint_trans, logged_transactions)
        print_json(cursor)
    except:
        print("Erro ao ler o arquivo input_log")
        exit(1)
