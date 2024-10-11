import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from email_obj import Email

class EmailSender:
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.connection = None

    def connect(self):
        '''Conecta ao servidor SMTP para enviar emails.'''
        self.connection = smtplib.SMTP('smtp.gmail.com', 587)
        self.connection.starttls()
        self.connection.login(self.email_address, self.password)
        print("Conectado ao servidor de envio")

    def send_email(self, email_obj: Email, destinatario: str):
        '''Envia um email a partir de um objeto Email e inclui o nome completo do remetente.'''
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = destinatario
        msg['Subject'] = 'Autorização Acesso'

        # Adiciona o corpo do email, incluindo o nome completo do aluno
        body_content = f"Nome completo do aluno: {email_obj.complete_name}\n\n{email_obj.body}"
        msg.attach(MIMEText(body_content, 'plain'))

        # Adiciona os anexos
        for attachment_path in email_obj.attachments:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as attachment:
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
                msg.attach(part)

        # Envia o email
        self.connection.sendmail(self.email_address, destinatario, msg.as_string())
        print(f"Email enviado para {destinatario}")

    def disconnect(self):
        '''Desconecta do servidor SMTP.'''
        if self.connection:
            self.connection.quit()
