from collector import EmailCollector
from reader import ler_arquivos_emails

if __name__ == "__main__":
    email_address = "maquinas902@gmail.com"
    password = "vjmm jseq feuk amhv"

    collector = EmailCollector(email_address, password)
    try:
        collector.connect()
        collector.fetch_emails()
    finally:
        collector.logout()

    pasta_coletada = '/home/wal/Auto/OO/collected'
    resultado_emails = ler_arquivos_emails(pasta_coletada)

    
    sender_email = "sender@gmail.com"
    sender_password = "password"
    recipient_email = "recipient@gmail.com"
    subject = "Hello from Python"
    body = "This email contains attachments."
    attachments = ["attachment.txt", "document.pdf", "image.jpg"]

    email_sender = EmailSender(sender_email, sender_password)
    email_sender.send_email(recipient_email, subject, body, attachments)

    

    
