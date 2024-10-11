import time
from collector import EmailCollector  # Classe para coletar emails
from reader import EmailReader  # Classe para ler os emails coletados
from sender import EmailSender  # Classe para enviar emails

# Configurações de email
email_address = "maquinas902@gmail.com"
password = "vjmm jseq feuk amhv"
destinatario = "walcandeia@gmail.com"

# Diretório base onde os emails são coletados
base_directory = '/home/wal/Auto/OO/collected'

def main():
    '''Roda a coleta de emails de forma contínua, processa e envia.'''
    collector = EmailCollector(email_address, password)
    reader = EmailReader()
    sender = EmailSender(email_address, password)

    try:
        while True:
            print("Conectando e coletando emails...")
            # Conecta e coleta emails
            collector.connect()
            collector.fetch_emails()
            collector.logout()

            print("Lendo emails coletados...")
            # Lê os emails recém-coletados a partir do base_directory
            emails = reader.ler_arquivos_emails(base_directory)

            if emails:
                for email_info in emails:
                    # Extrai os dados e os anexos do email lido
                    dados = email_info['dados']
                    anexos = email_info['anexos']

                    # Prepara o corpo do email a partir dos dados coletados
                    body = "\n".join(dados)
                    subject = f"Email processado: {dados[2]}" if len(dados) > 2 else "Assunto não encontrado"

                    # Envia o email para o destinatário
                    print(f"Enviando email para {destinatario}...")
                    sender.send_email(
                        recipient_email=destinatario,
                        subject= "Autorização de Acesso",
                        body=body,
                        attachments=anexos
                    )

            # Pausa a execução por um intervalo de tempo (ex: 5 minutos) antes de rodar novamente
            print("Aguardando 5 minutos para a próxima coleta...")
            time.sleep(300)  # Aguarda 5 minutos (300 segundos)
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        print("Finalizando o processo de coleta de emails.")

if __name__ == "__main__":
    main()
