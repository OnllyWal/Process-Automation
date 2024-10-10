import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def attach_file(self, filename: str, message: MIMEMultipart):
        '''Attach a file to the email message.'''
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename='{filename}'",
            )
            message.attach(part)

    def send_email(self, recipient_email: str, subject: str, body: str, attachments: list):
        '''Send an email with the specified subject, body, and attachments.'''
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = recipient_email
        
        message.attach(MIMEText(body))

        for attachment in attachments:
            self.attach_file(attachment, message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")

if __name__ == "__main__":
    sender_email = "sender@gmail.com"
    sender_password = "password"
    recipient_email = "recipient@gmail.com"
    subject = "Hello from Python"
    body = "This email contains attachments."
    attachments = ["attachment.txt", "document.pdf", "image.jpg"]

    email_sender = EmailSender(sender_email, sender_password)
    email_sender.send_email(recipient_email, subject, body, attachments)
