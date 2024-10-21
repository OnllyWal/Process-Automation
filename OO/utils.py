import pickle
from maquinas import usuarios

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

def processar_resposta(email, sent_emails, sender):
    corpo_email = email.crua  
    if "Nome completo do aluno:" in corpo_email:
        nome_aluno = corpo_email.split("Nome completo do aluno:")[1].split("\n")[0].strip()
        for email in sent_emails:
            if email.complete_name == nome_aluno:
                adress = email.email_name
                if "Autorizado" in corpo_email or "Autorizada" in corpo_email:
                    login, senha = gerar_login_senha(nome_aluno)
                    send_login_email(adress, login, senha, sender, email)
                elif "Negado" in corpo_email or "Negada" in corpo_email:
                    justificativa = corpo_email.split("Negada" or "Negado", 1)[1].split("\n")[0].strip()
                    send_negado_email(adress, justificativa, sender, email)

def gerar_login_senha(nome_aluno):
    arquivo_de_ips = "/home/wal/ProcessAutomation/Process-Automation/OO/ip.txt"
    login_novo = f"{nome_aluno.lower().replace(' ', '.')}"
    senha_novo = login_novo + "123"
    usuario_de_acesso = "fbro"
    senha_de_acesso="F!n0$BR0"
    return usuarios(arquivo_de_ips, usuario_de_acesso, senha_de_acesso, login_novo, senha_novo)

def send_login_email(adress, login, senha, sender, email):
    subject = "Seu login e senha"
    body = f"Olá,\n\nSeu login é: {login} e sua senha é: {senha}.\n\nAtenciosamente,\nEquipe"
    email.subject = subject
    email.body = body
    sender.send_email(email, adress)

def send_negado_email(adress, justificativa, sender, email):
    subject = "Ação Negada"
    body = f"Olá,\n\nSua solicitação foi negada. Justificativa: {justificativa}\n\nAtenciosamente,\nEquipe"
    email.subject = subject
    email.body = body
    sender.send_email(email, adress)
