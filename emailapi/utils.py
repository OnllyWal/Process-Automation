import pickle

def salvar_emails_em_arquivo(lista_emails, nome_arquivo='emails.pkl'):
    with open(nome_arquivo, 'wb') as f:
        pickle.dump(lista_emails, f)
    print(f"Lista de emails salva no arquivo {nome_arquivo}.")

def carregar_emails_de_arquivo(nome_arquivo='emails.pkl'):
    try:
        with open(nome_arquivo, 'rb') as f:
            lista_emails = pickle.load(f)
        print(f"Lista de emails carregada do arquivo {nome_arquivo}.")
        return lista_emails
    except FileNotFoundError:
        print(f"Nenhum arquivo encontrado com o nome {nome_arquivo}.")
        return []  
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o arquivo: {e}")
        return []