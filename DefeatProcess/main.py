from doc_editor import process_documents

input_directory = "/home/wal/ProcessAutomation/DefeatProcess/input"  # Substitua pelo caminho da pasta de entrada
output_directory = "/home/wal/ProcessAutomation/DefeatProcess/output"  # Substitua pelo caminho da pasta de saída

nome_coordenador = "Francisco de Assis Boldt"
numero_dia = "15"
nome_mes = "outubro"
numero_ano = "2024"
numero_sala = "503"
nome_completo_aluno = "Giancarlo Oliveira dos Santos"
titulo_tese = "MTS-POLKA: DIVISÃO DE TRÁFEGO MULTICAMINHOS EM PROPORÇÃO DE PESO COM ROTEAMENTO NA FONTE."
nome_orientador1 = "Profa. Dra. Cristina Klippel Dominicini"
nome_orientador2 = "Prof. Dr. Gilmar Luiz Vasssoler"
nome_membro_interno = "Prof. Dr. Leandro Colombi Resendo"
nome_membro_externo = "Prof. Dr. Vinícius Fernandes Soares Mota"


word_dict = {
    "nome_coordenador": nome_coordenador,
    "numero_dia": numero_dia,
    "nome_mes": nome_mes,
    "numero_ano": numero_ano,
    "numero_sala": numero_sala,
    "nome_completo_aluno": nome_completo_aluno,
    "titulo_tese": titulo_tese,
    "nome_orientador1": nome_orientador1,
    "nome_orientador2": nome_orientador2,
    "nome_membro_interno": nome_membro_interno,
    "nome_membro_externo": nome_membro_externo
}

process_documents(input_directory, output_directory, word_dict)
