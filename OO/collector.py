import imaplib
import email
import os

class EmailCollector:
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.connection = None

    def connect(self):
        '''Connects to the Gmail server.'''
        self.connection = imaplib.IMAP4_SSL("imap.gmail.com")
        self.connection.login(self.email_address, self.password)
        self.connection.select('inbox', readonly=False)  # Allow modifying the inbox (marking emails as read)

    def fetch_emails(self):
        '''Fetches all unread emails from the inbox.'''
        if self.connection is None:
            raise ConnectionError("You must connect first.")

        # Busca apenas os emails não lidos
        answers, ids = self.connection.search(None, 'UNSEEN')
        email_ids = ids[0].split()

        for num in email_ids:
            results, data = self.connection.fetch(num, '(RFC822)')
            text = data[0][1].decode('utf-8')
            msg = email.message_from_string(text)

            self.process_email(msg)  # Processa o email

            # Marca o email como lido
            self.connection.store(num, '+FLAGS', '\\Seen')

    def process_email(self, msg):
        '''Processes each email message.'''

        sender_name = msg['From'].split(" ")[0] if msg['From'] else "Unknown"
        subject_name = msg['Subject'] if msg['From'] else "Unknown"
        email_name = msg['From'].split(" ")[-1].strip('<>') if len(msg['From'].split(" ")) > 0 else "Unknown"
        complete_name = msg['From'].split('<')[0].strip()

        # Cria um diretório com base no remetente e um número sequencial
        unique_dir = self.create_unique_directory(sender_name)

        for part in msg.walk():
            if part.get_content_maintype() == 'text' and part.get_content_type() == 'text/plain':
                self.save_text(part, sender_name, subject_name, email_name, unique_dir, complete_name)
            elif part.get('Content-Disposition') is not None:
                self.save_attachment(part, unique_dir)

    def create_unique_directory(self, sender_name):
        '''Cria um diretório único para cada email baseado no remetente.'''
        base_dir = f'/home/wal/Auto/OO/collected/{sender_name}'
        os.makedirs(base_dir, exist_ok=True)

        # Encontra o próximo número disponível para o diretório
        count = 1
        unique_dir = os.path.join(base_dir, f"{sender_name} {count}")

        while os.path.exists(unique_dir):
            count += 1
            unique_dir = os.path.join(base_dir, f"{sender_name} {count}")

        # Cria o diretório único
        os.makedirs(unique_dir)
        return unique_dir

    def get_unique_file_name(self, directory, base_name, extension):
        '''Gera um nome de arquivo exclusivo, adicionando um número se necessário.'''
        count = 1
        file_name = f"{base_name}{extension}"
        file_path = os.path.join(directory, file_name)

        while os.path.exists(file_path):
            file_name = f"{base_name} ({count}){extension}"
            file_path = os.path.join(directory, file_name)
            count += 1

        return file_path

    def save_text(self, part, sender_name, subject_name, email_name, unique_dir, complete_name):
        '''Saves the text content of the email.'''
        if part.get_payload(decode=True) == b'\r\n':
            return

        # Gera um nome de arquivo exclusivo para os dados do email
        # Usando o nome do diretório para o arquivo de dados
        base_name = f'dados_{sender_name.split(" ")[0]}'  # Pega apenas o primeiro nome
        count = len(os.listdir(unique_dir))  # Conta quantos arquivos já existem para determinar o número
        file_path = self.get_unique_file_name(unique_dir, f'{base_name}{count + 1}', '.txt')  # Adiciona 1 ao count para o nome

        # Salva o conteúdo do email no arquivo
        with open(file_path, 'wb') as register:
            register.write(email_name.encode('utf-8'))
            register.write(b'\n')
            register.write(complete_name.encode('utf-8'))
            register.write(b'\n')
            register.write(subject_name.encode('utf-8'))
            register.write(b'\n')
            register.write(part.get_payload(decode=True))

    def save_attachment(self, part, unique_dir):
        '''Saves email attachments.'''
        filename = part.get_filename()
        if filename:
            # Gera um nome de arquivo exclusivo para o anexo
            attachment_path = self.get_unique_file_name(unique_dir, filename, '')

            # Salva o anexo
            with open(attachment_path, 'wb') as attachment:
                attachment.write(part.get_payload(decode=True))
            print(f"Anexo salvo: {attachment_path}")

    def logout(self):
        '''Logs out from the email server.'''
        if self.connection:
            self.connection.logout()

# Uso da classe
if __name__ == "__main__":
    email_address = "maquinas902@gmail.com"
    password = "vjmm jseq feuk amhv"

    collector = EmailCollector(email_address, password)
    try:
        collector.connect()
        collector.fetch_emails()
    finally:
        collector.logout()
