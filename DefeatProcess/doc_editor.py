import os
from docx import Document

def replace_words_in_document(doc, word_dict):
    """
    Substitui as palavras no dicionário em um documento Word.
    
    :param doc: O documento Word (objeto do python-docx).
    :param word_dict: Dicionário com as palavras a serem substituídas {palavra_antiga: palavra_nova}.
    """
    # Itera por todos os parágrafos
    for para in doc.paragraphs:
        # Verifica cada "run" (trecho de texto com formatação diferente)
        for run in para.runs:
            for old_word, new_word in word_dict.items():
                if old_word in run.text:
                    run.text = run.text.replace(old_word, new_word)

def process_documents(input_dir, output_dir, word_dict):
    """
    Processa todos os documentos .docx na pasta de entrada e salva os arquivos modificados na pasta de saída.
    
    :param input_dir: Caminho da pasta com os documentos .docx de entrada.
    :param output_dir: Caminho da pasta para salvar os documentos modificados.
    :param word_dict: Dicionário com as palavras a serem substituídas {palavra_antiga: palavra_nova}.
    """
    # Verificar se a pasta de saída existe, caso contrário, cria
    os.makedirs(output_dir, exist_ok=True)

    # Iterar por todos os arquivos na pasta de entrada
    for filename in os.listdir(input_dir):
        if filename.endswith(".docx"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Carregar o documento Word
            doc = Document(input_path)

            # Substituir as palavras conforme o dicionário
            replace_words_in_document(doc, word_dict)

            if filename == "Modelo Ata de Defesa.docx":
                local_dict = {"resultado":"APROVADO"}
                replace_words_in_document(doc, local_dict)
                approved_filename = f"{os.path.splitext(os.path.basename(output_path))[0]}_APROVADO.docx"
                approved_path = os.path.join(output_dir, approved_filename)
                doc.save(approved_path)

                local_dict = {"APROVADO":"REPROVADO"}
                replace_words_in_document(doc, local_dict)
                repproved_filename = f"{os.path.splitext(os.path.basename(output_path))[0]}_REPROVADO.docx"
                repproved_path = os.path.join(output_dir, repproved_filename)
                doc.save(repproved_path)
            else:
                doc.save(output_path)