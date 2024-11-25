import re
from defesa.doc_process import process_documents

def start_doc_process(string):
    # Inicializa o dicionário com valores padrão
    word_dict = {
        "nome_coordenador": "Francisco de Assis Boldt",
        "numero_dia": "",
        "nome_mes": "",
        "numero_ano": "",
        "numero_hora": "",
        "numero_sala": "",
        "link_sala": "",
        "nome_completo_aluno": "",
        "titulo_tese": "",
        "nome_orientador1": "",
        "nome_orientador2": "",
        "nome_membro_interno": "",
        "nome_membro_externo": ""
    }

    # Define expressões regulares para capturar os valores
    padroes = {
        "nome_completo_aluno": r"(Aluno|Nome Completo Aluno:)\s*(.+)",
        "titulo_tese": r"Título:\s*(.+)",
        "data": r"Data:\s*(\d{2})/(\d{2})/(\d{4})",
        "numero_hora": r"Horário:\s*(\d{2}:\d{2})",
        "numero_sala": r"Sala:\s*(.+)",
        "link_sala": r"(Link Sala Virtual|Link da video chamada:)\s*(.+)",
        "nome_orientador1": r"(Orientador:|Orientador Principal)\s*(.+)",
        "nome_orientador2": r"Coorientador:\s*(.+)",
        "nome_membro_interno": r"(Membro Interno:|Avaliador Interno:)\s*(.+)",
        "nome_membro_externo": r"(Membro Externo|Avaliador Interno:)\s*(.+)"
    }

    # Captura os valores com base nos padrões
    for chave, padrao in padroes.items():
        match = re.search(padrao, string)
        if match:
            if chave == "data":  # Processa a data separadamente
                word_dict["numero_dia"], numero_mes, word_dict["numero_ano"] = match.groups()
                word_dict["nome_mes"] = obter_nome_mes(numero_mes)
            else:
                word_dict[chave] = match.group(1).strip()
    
    doc_list = process_documents(word_dict)
    return doc_list

def obter_nome_mes(numero_mes):
    # Mapeia números de mês para nomes
    meses = {
        "01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril",
        "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
        "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
    }
    return meses.get(numero_mes, "")
