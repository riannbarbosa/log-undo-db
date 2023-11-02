import re
from file_read_backwards import FileReadBackwards
from config.print import print_transactions, print_json, print_update


uncommited_trans = []
str_file_backward = ''
str_file = ''
# encontra end checkpoint de tras para frente
#se tiver start checkpoint antes do end checkpoint, ele para

def getStr_Backward(file_path):
    with FileReadBackwards(file_path, encoding="utf-8") as file:
        str_file_backward= ''.join(file)
    return str_file_backward

def getStr(file_path):
    file = open(file_path, 'r')
    str_file= ''.join(file)
    return str_file

def find_by_last_checkpoint_find(file_path):
        with FileReadBackwards(file_path, encoding="utf-8") as file:
            commit_regex = ''
            for line in file:
                line = re.sub('\n|\r', '', line).strip()
                if "END CKPT" in line:
                    break
                if 'start' in line:
                    transaction = line[-3:-1]
                    commit_regex = r"<commit {}>".format(transaction)
                    dont_have = not re.search(commit_regex, getStr_Backward(file_path))
                    if(dont_have):
                         uncommited_trans.append(transaction)
        return uncommited_trans[::-1]
                    

# encontra transacoes comitadas antes do start ckpt  
# como esta antes do start ckpt, nao precisa fazer undo pois nao 
# importa mais o que aconteceu antes do start ckpt
# def find_commited_trans(file_path):
#     file = open(file_path, 'r')
#     try:
#         for line in file:
#                 if "START CKPT" in line:
#                     break
#                 if 'start' in line:
#                     transaction = line[-4:-2]
#                     commit_regex = r"<commit {}>".format(transaction)
#                     dont_have = not re.search(commit_regex, getStr(file_path))
#                     if(dont_have):
#                          uncommited_trans.append(transaction)
#                 print(uncommited_trans)
#         return uncommited_trans[::-1]
#     finally:
#          file.close()

def undo_changes(file_path, cursor):
        file = open(file_path, 'r')

        try:
            for transaction in uncommited_trans:
                file.seek(0)
                content = file.read()
                start_transaction = content.index('<start '+ transaction +'>')
                file.seek(start_transaction)
                for line in file:
                    matches = re.search('<'+ transaction +',(.+?)>', line)
                    if('<commit '+ transaction +'>' in line):
                         continue
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
        getStr(file)
        getStr_Backward(file)
       # find_commited_trans(file)
        checkpoint_trans = find_by_last_checkpoint_find(file)
        undo_changes(file, cursor)

        print_transactions(checkpoint_trans)
        print_json(cursor)
    except Exception as e:
        print(f"Error reading the input_log file: {str(e)}")
        exit(1)
