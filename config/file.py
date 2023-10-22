import json

def file_metadata():
    data = None
    try: 
        file_path = open('files/metadata.json', 'r')
        data = json.load(file_path)['INITIAL']
    except:
        print("Erro ao ler arquivo de metadados.")
        exit(1)
    finally:
        file_path.close()
    return list(zip(data['A'], data['B']))
