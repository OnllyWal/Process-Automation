import imaplib
import email as email_lib
import os
from email_obj import Email

class EmailCollector:
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.connection = None
        self.emails = []  # Lista para armazenar objetos da classe Email

    def connect(self):
        '''Connects to the Gmail server.'''
        self.connection = imaplib.IMAP4_SSL("imap.gmail.com")
        self.connection.login(self.email_address, self.password)
        self.connection.select('inbox', readonly=False)  # Permite modificar a caixa de entrada (marcar emails como lidos)

    def fetch_emails(self):
        '''Fetches all unread emails from the inbox and creates Email objects.'''
        if self.connection is None:
            raise ConnectionError("You must connect first.")

        # Busca apenas os emails não lidos
        answers, ids = self.connection.search(None, 'UNSEEN')
        email_ids = ids[0].split()

        for num in email_ids:
            results, data = self.connection.fetch(num, '(RFC822)')
            text = data[0][1].decode('utf-8')
            msg = email_lib.message_from_string(text)

            email_obj = self.process_email(msg)  # Processa o email e retorna um objeto Email
            if email_obj:
                self.emails.append(email_obj)  # Adiciona o objeto Email à lista

            # Marca o email como lido
            self.connection.store(num, '+FLAGS', '\\Seen')

    def process_email(self, msg):
        '''Processes each email message and returns an Email object.'''
        sender_name = msg['From'].split(" ")[0] if msg['From'] else "Unknown"
        subject_name = msg['Subject'] if msg['From'] else "Unknown"
        email_name = msg['From'].split(" ")[-1].strip('<>') if len(msg['From'].split(" ")) > 0 else "Unknown"
        complete_name = msg['From'].split('<')[0].strip()

        attachments = []  # Lista para armazenar os caminhos dos anexos
        email_body = ''  # String para armazenar o corpo do email

        # Processa as partes do email
        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_type() == 'text/plain':
                email_body = part.get_payload(decode=True).decode('utf-8')  # Captura o corpo do email
            elif part.get('Content-Disposition') is not None:
                attachment_path = self.save_attachment(part, sender_name)
                if attachment_path:
                    attachments.append(attachment_path)

        # Cria e retorna um objeto Email
        return Email(sender_name, complete_name, email_name, subject_name, email_body, attachments)

    def save_attachment(self, part, sender_name):
        '''Saves email attachments and returns the path of the saved file.'''
        filename = part.get_filename()
        if filename:
            base_dir = f'/home/wal/Auto/OO/collected/{sender_name}'
            os.makedirs(base_dir, exist_ok=True)

            # Gera um caminho de arquivo único para o anexo
            attachment_path = os.path.join(base_dir, filename)
            count = 1

            while os.path.exists(attachment_path):
                attachment_path = os.path.join(base_dir, f"{filename.split('.')[0]}_{count}.{filename.split('.')[-1]}")
                count += 1

            # Salva o anexo
            with open(attachment_path, 'wb') as attachment:
                attachment.write(part.get_payload(decode=True))

            print(f"Anexo salvo: {attachment_path}")
            return attachment_path
        return None

    def logout(self):
        '''Logs out from the email server.'''
        if self.connection:
            self.connection.logout()