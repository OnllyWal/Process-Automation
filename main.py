import time
from emailapi.collector import EmailCollector  # Classe EmailCollector já implementada
from emailapi.sender import EmailSender  # Classe EmailSender já implementada
from acesso.acesso import processar_resposta_acesso
from emailapi.utils import carregar_emails_de_arquivo, salvar_emails_em_arquivo
from defesa.pre_process import start_doc_process
from defesa.text_chamado import text_chamado
from emailapi.email_obj import Email
from defesa.doc_process import remove_docs

def main():
    # Informações de login
    sent_emails = carregar_emails_de_arquivo(nome_arquivo='/home/wal/ProcessAutomation/ISOEmailAPI/emailapi/emails.pkl') 

    email_address = 'maquinas902@gmail.com' #email para coleta
    password = 'vjmm jseq feuk amhv' #senha email de coleta
    destinatario = 'ppcomp.ifes@gmail.com' #email para autorização

    # Configuração do coletor e do sender
    collector = EmailCollector(email_address, password)
    sender = EmailSender(email_address, password)

    # Conecta ao servidor SMTP
    sender.connect()

    while True:
        #Coleta Emails, cria objetos e armazena na lista collector.emails
        print("Coletando novos emails...")
        collector.connect()
        collector.fetch_emails()

        if collector.emails:
            print(f"{len(collector.emails)} emails coletados. Processando...")
            for email_obj in collector.emails:

                if email_obj not in sent_emails:
                
                    #Se o endereço de email for do coordenador, processa como resposta
                        if email_obj.email_name == destinatario:
                        processar_resposta_acesso(email_obj, sent_emails, sender)
                    
                        if ("Preenchimento Dados Defesa" in email_obj.subject):
                            documentos = start_doc_process(email_obj.body)
                            text = text_chamado(email_obj.body)
                            if not documentos:
                                print("Nenhum documento encontrado na pasta.")
                                return

                            email_obj_coord = Email(
                                sender_name = "Equipe",
                                complete_name= "Equipe PPComp",
                                email_name= "maquinas902@gmail.com",
                                subject= "Abertura de Chamado",
                                raw= email_obj.raw,
                                body=f"{text}\n\nAtenciosamente,\nSua equipe.",
                                attachments=documentos
                            )
                            email_obj_age = Email(
                                sender_name = "Equipe",
                                complete_name= "Equipe PPComp",
                                email_name= "maquinas902@gmail.com",
                                subject= "Abertura de Chamado",
                                raw= email_obj.raw,
                                body = f"Segue Lista de Documentos para futura abertura de Processo no SIPAC",
                                attachments=documentos
                            )
                            sender.send_email(email_obj_coord, destinatario)
                            sender.send_email(email_obj_age, email_obj.email_name)
                            remove_docs(documentos)

                        
                        #Se o título for identificado como Defesa, inicia o processo da Defesa
                        if ("Defesa" in email_obj.subject) or ("Banca" in email_obj.subject):
                            agente = email_obj.complete_name
                            adress = email_obj.email_name
                            email_obj.sender_name = "Equipe"
                            email_obj.complete_name = "Equipe PPComp"
                            email_obj.subject = "Preenchimento Dados Defesa"
                            email_obj.body = '''

                            Nome Completo Aluno: 
                            Título: 
                            Data: dd/mm/aaaa
                            Horário: 00:00h
                            Sala: (N° da Sala ou "Virtual")
                            Link Sala Virtual(Se n houver, deixar em branco):

                            Orientador Principal: 
                            Coorientador: 
                            Membro Interno: 
                            Membro Externo: 
                            '''
                            
                            sender.send_email(email_obj, adress)
                            sent_emails.append(email_obj)
                            print(f"Email do tipo Defesa enviado de {agente} para {destinatario}.")
                            

                        #Se o título for indentificado como Acesso, inicia o processo de Acesso
                        if ("Acesso" in email_obj.subject) or ("Computador" in email_obj.subject):
                            name_aluno = email_obj.complete_name
                            email_obj.sender_name = "Equipe"
                            email_obj.complete_name = "Equipe PPComp"
                            email_obj.subject = "Autorização Acesso"
                            email_obj.body = f'''

                            Nome Completo Aluno: {name_aluno}
                            '''
                            sender.send_email(email_obj, destinatario)
                            sent_emails.append(email_obj)
                            print(f"Email do tipo Acesso enviado de {name_aluno} para {destinatario}.")
                            time.sleep(30)

            collector.emails.clear()
            print("Lista de emails coletados esvaziada.")
        else:
            print("Nenhum novo email coletado.")

        collector.logout()
        salvar_emails_em_arquivo(sent_emails, '/home/wal/ProcessAutomation/Process-Automation/OO/emails.pkl')
        time.sleep(30)

    sender.disconnect()

if __name__ == "__main__":
    main()
