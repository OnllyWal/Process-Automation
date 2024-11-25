class Email:
    def __init__(self, sender_name: str, complete_name: str, email_name: str, subject: str, body: str, attachments: list, raw):
        self.sender_name = sender_name
        self.complete_name = complete_name
        self.email_name = email_name
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.raw = raw

    def __repr__(self):
        return (f"Email(sender_name={self.sender_name}, complete_name={self.complete_name}, "
                f"email_name={self.email_name}, subject={self.subject}, attachments={self.attachments})")
