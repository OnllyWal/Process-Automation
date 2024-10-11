import paramiko
'''
Cria um novo usuário em múltiplos servidores remotos.

    Parâmetros:
    - arquivo_de_ips (str): Caminho para um arquivo com uma lista de endereços IP. 
                             Cada IP deve estar em uma linha separada.
    - usuario_de_acesso (str): Nome do usuário para autenticação nas máquinas remotas.
                               Deve ter permissões sudo para criar novos usuários.
    - senha_de_acesso (str): Senha do usuário de acesso para autenticação SSH.
    - usuario_novo (str): Nome do novo usuário a ser criado em cada servidor.
                          Deve ser único para cada servidor.
    - senha_novo (str): Senha a ser atribuída ao novo usuário.
    
'''

def usuarios(arquivo_de_ips, usuario_de_acesso, senha_de_acesso, usuario_novo, senha_novo):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Leitura de ips
    arquivo = open(arquivo_de_ips, "r")
    lista_de_ips = []
    for ip in arquivo:
        ip = ip.strip()
        lista_de_ips.append(ip)
    arquivo.close()
    command = f"echo '{senha_de_acesso}' | sudo -S useradd -m -s /bin/bash {usuario_novo} && echo '{usuario_novo}:{senha_novo}' | sudo chpasswd"

    for ip in lista_de_ips:
        try:
            # Tentativa de conexão
            print(f"Tentando conectar ao {ip}...")
            client.connect(ip, username=usuario_de_acesso, password=senha_de_acesso)
            print(f"Conectado ao {ip}")

            comando_verificar_user = f"id {usuario_novo} >/dev/null 2>&1; echo $?"
            stdin, stdout, stderr = client.exec_command(comando_verificar_user)
            usuario_existente = int(stdout.read().decode().strip()) == 0

            if (usuario_existente):
                print(f"O usuário '{usuario_novo}' já existe no {ip}.")
            else:
                # Executa comando remoto
                stdin, stdout, stderr = client.exec_command(command)
                
                if(stderr.read().decode()):
                    print(f"Erro ao criar o usuário '{usuario_novo}' no {ip}: {stderr.read().decode()}")
                    
                else:
                    print(f"O usuário '{usuario_novo}' criado no {ip}.")
            
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print(f"Não foi possível conectar ao {ip}: {str(e)}")
        
        except Exception as e:
            # Captura outros tipos de exceções que possam ocorrer
            print(f"Erro ao tentar conectar ao {ip}: {str(e)}")
        
        finally:
            try:
                client.close()  # Fecha a conexão se estiver aberta
            except:
                pass  # Se não conseguiu conectar, ignora o fechamento