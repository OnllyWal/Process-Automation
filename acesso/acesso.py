from acesso.maquinas import usuarios

#Processa a Resposta do Coordenador
def processar_resposta_acesso(email, sent_emails, sender):
    corpo_email = email.raw  
    #Verifica se o email é uma resposta de pedido de acesso
    if "Nome completo do aluno:" in corpo_email:
        
        #Guarda o nome do aluno que está sendo verificado
        nome_aluno = corpo_email.split("Nome completo do aluno:")[1].split("\n")[0].strip()

        #Procura nos email guardados em arquivo o email do aluno, para enviar a resposta
        for email in sent_emails:
            if email.complete_name == nome_aluno:
                adress = email.email_name

                #Se a reposta é autorizado, envia o login
                if "Autorizado" in corpo_email or "Autorizada" in corpo_email:
                    login, senha = gerar_login_senha(nome_aluno)
                    subject = "Seu login e senha"
                    body = f"Olá,\n\nSeu login é: {login} e sua senha é: {senha}.\n\nAtenciosamente,\nEquipe"
                    email.subject = subject
                    email.body = body
                    sender.send_email(email, adress)

                #Se a reposta é negado, envia a justificativa
                elif "Negado" in corpo_email or "Negada" in corpo_email:
                    justificativa = corpo_email.split("Negada" or "Negado", 1)[1].split("\n")[0].strip()
                    subject = "Ação Negada"
                    body = f"Olá,\n\nSua solicitação foi negada. Justificativa: {justificativa}\n\nAtenciosamente,\nEquipe"
                    email.subject = subject
                    email.body = body
                    sender.send_email(email, adress)

#Gera login e Senha do aluno
def gerar_login_senha(nome_aluno):
    arquivo_de_ips = "/home/wal/ProcessAutomation/ISOEmailAPI/acesso/ip.txt"
    login_novo = f"{nome_aluno.lower().replace(' ', '.')}"
    senha_novo = login_novo + "123"
    usuario_de_acesso = "fbro"
    senha_de_acesso="F!n0$BR0"
    return usuarios(arquivo_de_ips, usuario_de_acesso, senha_de_acesso, login_novo, senha_novo)
