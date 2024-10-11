import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import hashlib  # Para criar um hash dos e-mails enviados

class EmailSender:
    def __init__(self, sender_email: str, sender_password: str, log_file="emails_enviados.txt"):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.log_file = log_file  # Arquivo que mantém registro dos emails enviados

    def attach_file(self, filepath: str, message: MIMEMultipart):
        '''Attach a file to the email message using the original file name as the attachment name.'''
        try:
            with open(filepath, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)  # Pega apenas o nome do arquivo, sem o caminho completo
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                message.attach(part)
        except Exception as e:
            print(f"Erro ao anexar o arquivo {filepath}: {e}")

    def email_was_sent(self, subject, recipient_email):
        '''Check if an email with the same subject and recipient was already sent.'''
        email_id = self.generate_email_id(subject, recipient_email)
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                sent_emails = file.read().splitlines()
            return email_id in sent_emails
        return False

    def log_sent_email(self, subject, recipient_email):
        '''Log the subject and recipient of the email as sent.'''
        email_id = self.generate_email_id(subject, recipient_email)
        with open(self.log_file, 'a') as file:
            file.write(f"{email_id}\n")

    def generate_email_id(self, subject, recipient_email):
        '''Generate a unique identifier for an email based on its subject and recipient.'''
        return hashlib.sha256(f"{subject}{recipient_email}".encode()).hexdigest()

    def send_email(self, recipient_email: str, subject: str, body: str, attachments: list):
        '''Send an email with the specified subject, body, and attachments, if it has not been sent already.'''
        if self.email_was_sent(subject, recipient_email):
            print(f"O email com o assunto '{subject}' já foi enviado para {recipient_email}. Não será enviado novamente.")
            return

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = recipient_email
        
        # Add the body text to the email
        message.attach(MIMEText(body, "plain"))

        # Attach each file in the attachments list
        for attachment in attachments:
            self.attach_file(attachment, message)

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            print(f"Email enviado com sucesso para {recipient_email}!")

            # Log the sent email
            self.log_sent_email(subject, recipient_email)
        except Exception as e:
            print(f"Erro ao enviar email: {e}")

# Exemplo de uso
if __name__ == "__main__":
    sender_email = "sender@gmail.com"
    sender_password = "password"
    recipient_email = "recipient@gmail.com"
    subject = "Hello from Python"
    body = "This email contains attachments."
    attachments = ["/caminho/para/arquivo1.txt", "/caminho/para/arquivo2.pdf", "/caminho/para/imagem.jpg"]

    email_sender = EmailSender(sender_email, sender_password)
    email_sender.send_email(recipient_email, subject, body, attachments)
