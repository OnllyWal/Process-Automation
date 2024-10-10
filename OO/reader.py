import os

def ler_arquivos_emails(pasta):
    '''Lê arquivos de emails salvos em pastas separadas por remetente e retorna um dicionário com dados e anexos.'''
    resultado = []  # Usando uma lista para armazenar dados e anexos

    # Itera sobre cada pasta de remetente
    for sender_folder in os.listdir(pasta):
        sender_path = os.path.join(pasta, sender_folder)
        print(f"Verificando a pasta: {sender_path}")

        # Verifica se é um diretório
        if os.path.isdir(sender_path):
            # Itera sobre cada subpasta (que representa um email enviado)
            for subfolder in os.listdir(sender_path):
                subfolder_path = os.path.join(sender_path, subfolder)
                print(f"Verificando subpasta: {subfolder_path}")

                # Verifica se é um diretório (subpasta)
                if os.path.isdir(subfolder_path):
                    # O arquivo de dados deve estar com o nome da subpasta
                    dados_email_path = os.path.join(subfolder_path, f'dados_{subfolder}.txt')
                    print(f"Procurando arquivo: {dados_email_path}")

                    # Lê o conteúdo do arquivo de dados, se existir
                    if os.path.isfile(dados_email_path):
                        with open(dados_email_path, 'r', encoding='utf-8') as file:
                            conteudo = file.readlines()
                            # Remove quebras de linha e espaços em branco
                            conteudo = [linha.strip() for linha in conteudo]
                            dados = {
                                'dados': conteudo,
                                'anexos': []
                            }
                            resultado.append(dados)  # Adiciona os dados à lista

                            print(f"Conteúdo do arquivo {dados_email_path}: {conteudo}")
                    else:
                        print(f"Arquivo de dados não encontrado para {subfolder}.")

                    # Verifica se existem anexos na subpasta
                    for anexo in os.listdir(subfolder_path):
                        anexo_path = os.path.join(subfolder_path, anexo)
                        # Adiciona o caminho do anexo à lista de anexos
                        if os.path.isfile(anexo_path) and anexo != f'dados_{subfolder}.txt':
                            dados['anexos'].append(anexo_path)  # Armazenar o caminho completo do anexo
                            print(f"Anexo encontrado: {anexo_path}")

    return resultado

# Exemplo de uso
pasta_coletada = '/home/wal/Auto/OO/collected'
resultado_emails = ler_arquivos_emails(pasta_coletada)

# Imprime o resultado
for email_info in resultado_emails:
    print("\nDados:")
    for linha in email_info['dados']:
        print(f" - {linha}")
    print("Anexos:")
    for anexo in email_info['anexos']:
        print(f" - {anexo}")
