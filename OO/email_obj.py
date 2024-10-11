class Email:
    def __init__(self, sender_name: str, complete_name: str, email_name: str, subject: str, body: str, attachments: list, crua):
        """
        Inicializa um objeto Email com os detalhes do remetente, assunto, corpo e anexos.
        
        :param sender_name: Nome simplificado do remetente.
        :param complete_name: Nome completo do remetente.
        :param email_name: Endereço de email do remetente.
        :param subject: Assunto do email.
        :param body: Corpo do email.
        :param attachments: Lista de caminhos dos anexos do email.
        """
        self.sender_name = sender_name
        self.complete_name = complete_name
        self.email_name = email_name
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.crua = crua

    def __repr__(self):
        return (f"Email(sender_name={self.sender_name}, complete_name={self.complete_name}, "
                f"email_name={self.email_name}, subject={self.subject}, attachments={self.attachments})")
