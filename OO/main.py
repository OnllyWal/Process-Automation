import time
from collector import EmailCollector  # Classe EmailCollector já implementada
from sender import EmailSender  # Classe EmailSender já implementada
from email_obj import Email
from maquinas import usuarios
import pickle
def main():
    # Informações de login
    carregar_emails_de_arquivo(nome_arquivo='/home/wal/ProcessAutomation/Process-Automation/OO/emails.pkl') 

    email_address = 'maquinas902@gmail.com'
    password = 'vjmm jseq feuk amhv'
    destinatario = 'walcandeia@gmail.com'

    # Configuração do coletor e do sender
    collector = EmailCollector(email_address, password)
    sender = EmailSender(email_address, password)
    
    # Conecta ao servidor SMTP
    sender.connect()

    # Lista de emails já enviados
    sent_emails = []
    print(sent_emails)

    while True:
        print("Coletando novos emails...")

        # Conectar ao servidor de email e coletar os novos emails
        collector.connect()
        collector.fetch_emails()

        # Verifica se há emails coletados
        if collector.emails:
            print(f"{len(collector.emails)} emails coletados. Processando...")

            # Processa cada email coletado
            for email_obj in collector.emails:
                # Verifica se o email coletado é uma resposta do destinatário
                if email_obj.email_name == destinatario:
                    print("resposta")
                    # Processa a resposta do destinatário
                    processar_resposta(email_obj,sent_emails, sender)
                else:
                    # Envia o email para o destinatário
                    if email_obj not in sent_emails:
                        sender.send_email(email_obj, destinatario)
                        sent_emails.append(email_obj)  # Adiciona o email à lista de emails já enviados
                        print(f"Email enviado de {email_obj.complete_name} para {destinatario}.")

            # Limpa a lista de emails coletados para a próxima rodada
            collector.emails.clear()
            print("Lista de emails coletados esvaziada.")
        else:
            print("Nenhum novo email coletado.")

        # Desconecta do servidor de email
        collector.logout()
        salvar_emails_em_arquivo(sent_emails, '/home/wal/ProcessAutomation/Process-Automation/OO/emails.pkl')
        # Espera 1 minuto antes de coletar novamente
        time.sleep(60)

    # Desconecta do servidor SMTP
    
    sender.disconnect()

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
        return []  # Retorna uma lista vazia se o arquivo não existir
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o arquivo: {e}")
        return []

def processar_resposta(email, sent_emails, sender):
    corpo_email = email.crua  # Acessa o conteúdo do corpo do email
    print(email.crua)

    # Busca pelo nome completo do aluno no corpo da mensagem
    if "Nome completo do aluno:" in corpo_email:
        nome_aluno = corpo_email.split("Nome completo do aluno:")[1].split("\n")[0].strip()
        print(nome_aluno)
        for email in sent_emails:
            if email.complete_name == nome_aluno:
                adress = email.email_name
                print(adress)
                print(email.body)
                if "Autorizado" in corpo_email or "Autorizada" in corpo_email:
                    print(f"Ação autorizada para o aluno: {nome_aluno}.")
                    
                    # Chama a função para gerar login e senha
                    login, senha = gerar_login_senha(nome_aluno)
                    print(login, senha)
                    # Envia o e-mail com login e senha
                    print("ta enviando")
                    send_login_email(adress, login, senha, sender)
                
                elif "Negado" in corpo_email or "Negada" in corpo_email:
                    trecho = corpo_email.split("Negada" or "Negado", 1)[1]  # Pega o texto após a palavra
                    # Divide o trecho até a próxima quebra de linha
                    resultado = trecho.split("\n", 1)[0]  # Pega a parte antes da quebra de linha
                    justificativa = resultado.strip()
                    print(f"Ação negada para o aluno: {nome_aluno}. Justificativa: {justificativa}")
                    
                    # Envia o e-mail com a justificativa
                    send_negado_email(adress, justificativa)
        # Aqui você pode adicionar a ação apropriada para uma negativa
    else:
        nome_aluno = "Desconhecido"

# Função para gerar login e senha (use seu código já existente)
def gerar_login_senha(nome_aluno):
    arquivo_de_ips = "/home/wal/ProcessAutomation/Process-Automation/OO/ip.txt"
    login_novo = f"{nome_aluno.lower().replace(' ', '.')}"
    senha_novo = login_novo + "123"
    usuario_de_acesso = "wal"
    senha_de_acesso="wal123"
    login, senha = usuarios(arquivo_de_ips,usuario_de_acesso, senha_de_acesso,login_novo, senha_novo)
    return login, senha

# Função para enviar o e-mail com login e senha
def send_login_email(adress, login, senha, sender):
    subject = "Seu login e senha"
    body = f"Olá,\n\nSeu login é: {login} e sua senha é: {senha}.\n\nAtenciosamente,\nEquipe"
    # Aqui você pode chamar a função de envio de e-mail, substituindo pelos valores adequados

    email_obj = Email(subject=subject, body=body)
    sender.send_email(email_obj, adress)
    print(f"Email enviado para {adress} com login e senha.")

# Função para enviar o e-mail com a justificativa de negação
def send_negado_email(adress, justificativa, sender):
    subject = "Ação Negada"
    body = f"Olá,\n\nSua solicitação foi negada. Justificativa: {justificativa}\n\nAtenciosamente,\nEquipe"
    # Aqui você pode chamar a função de envio de e-mail, substituindo pelos valores adequados
    email_obj = Email(subject=subject, body=body)
    sender.send_email(email_obj, adress)
    print(f"Email enviado para {adress} com justificativa de negação.")

if __name__ == "__main__":
    main()
