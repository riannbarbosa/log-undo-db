import re
from file_read_backwards import FileReadBackwards
from config.print import print_transactions, print_json, print_update


uncommited_trans = []
commited_trans = []
# encontra end checkpoint de tras para frente
#se tiver start checkpoint antes do end checkpoint, ele para
def find_by_last_checkpoint_find(file_path):
        with FileReadBackwards(file_path, encoding="utf-8") as file:

            for line in file:
                line = re.sub('\n|\r', '', line).strip()
                if "END CKPT" in line:
                    break
                    
                matches = re.search(r'<start (.+?)>', line)
                if matches:
                   uncommited_trans.append(matches.group(1))
            return uncommited_trans[::-1]

# encontra transacoes comitadas antes do start ckpt 
def find_commited_trans(file_path):
    commited= False
    file = open(file_path, 'r')
    try:
        for line in file:
                if "START CKPT" in line:
                    break
                matches = re.search(r'<commit (.+?)>', line)
                if matches:
                    commited_trans.append(matches.group(1))
                    commited = True
                else:
                    commited = False
        return commited
    finally:
         file.close()

def find_if_not_committed(file_path):
    file = open(file_path, 'r')
        
    try:
        for line in file:
            if "END CKPT" in line:
                    break
            if(find_commited_trans(file_path) == False):
                matches = re.search(r'<start (.+?)>', line)
                if matches:
                        uncommited_trans.append(matches.group(1))
            return uncommited_trans[::-1]
    finally:
         file.close()


def undo_changes(file_path, cursor):
        file = open(file_path, 'r')
        try:
             
            for transaction in uncommited_trans:
                file.seek(0)
                
                content = file.read()
                start_transaction = content.index('<start '+ transaction +'>')
                file.seek(start_transaction)
                for line in file:
                    if ('<commit '+ transaction +'>' in line): break
                    matches = re.search('<'+ transaction +',(.+?)>', line)
                    if matches:
                        values = matches.group(1).split(',')
                        cursor.execute('SELECT ' + values[1] + ' FROM data_log WHERE id = ' + values[0])
                        tuple = cursor.fetchone()[0]
                        if(int(values[2]) != tuple):
                            cursor.execute(f'UPDATE data_log SET {values[1]} = {values[2]} WHERE id = {values[0]}')
                            print_update(transaction, tuple, values)
        finally:
             file.close()

def read_log(cursor):
    file = 'files/input_log'
    try:
        checkpoint_trans = find_by_last_checkpoint_find(file)
        uncommitted_transactions = find_if_not_committed(file)
        undo_changes(file, cursor)
        print_transactions(checkpoint_trans,  uncommitted_transactions)
        print_json(cursor)
    except Exception as e:
        print(f"Error reading the input_log file: {str(e)}")
        exit(1)
