import time
from collector import EmailCollector  # Classe EmailCollector já implementada
from sender import EmailSender  # Classe EmailSender já implementada
from utils import carregar_emails_de_arquivo, salvar_emails_em_arquivo, processar_resposta

def main():
    # Informações de login
    sent_emails = carregar_emails_de_arquivo(nome_arquivo='/home/wal/ProcessAutomation/Process-Automation/OO/emails.pkl') 

    email_address = 'maquinas902@gmail.com'
    password = 'vjmm jseq feuk amhv'
    destinatario = 'walcandeia@gmail.com'

    # Configuração do coletor e do sender
    collector = EmailCollector(email_address, password)
    sender = EmailSender(email_address, password)

    # Conecta ao servidor SMTP
    sender.connect()

    while True:
        print("Coletando novos emails...")
        collector.connect()
        collector.fetch_emails()

        if collector.emails:
            print(f"{len(collector.emails)} emails coletados. Processando...")
            for email_obj in collector.emails:
                if email_obj.email_name == destinatario:
                    processar_resposta(email_obj, sent_emails, sender)
                else:
                    if email_obj not in sent_emails:
                        sender.send_email(email_obj, destinatario)
                        sent_emails.append(email_obj)
                        print(f"Email enviado de {email_obj.complete_name} para {destinatario}.")
                        time.sleep(30)

            collector.emails.clear()
            print("Lista de emails coletados esvaziada.")
        else:
            print("Nenhum novo email coletado.")

        collector.logout()
        salvar_emails_em_arquivo(sent_emails, '/home/wal/ProcessAutomation/Process-Automation/OO/emails.pkl')
        time.sleep(30)

    sender.disconnect()

if __name__ == "__main__":
    main()
