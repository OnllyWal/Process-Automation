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

def list_doc(caminho_pasta: str) -> list[str]:
    '''Lista todos os documentos em uma pasta.'''
    return [
        os.path.join(caminho_pasta, arquivo)
        for arquivo in os.listdir(caminho_pasta)
        if os.path.isfile(os.path.join(caminho_pasta, arquivo))
    ]

def remove_docs(documentos: list[str]):
    '''Apaga os documentos listados.'''
    for documento in documentos:
        try:
            os.remove(documento)
            print(f"Arquivo removido: {documento}")
        except Exception as e:
            print(f"Erro ao remover {documento}: {e}")

def process_documents(word_dict):
    
    #Caminhos Pastas
    input_dir = "/home/wal/ProcessAutomation/ISOEmailAPI/defesa/input"  # Substitua pelo caminho da pasta de entrada
    output_dir = "/home/wal/ProcessAutomation/ISOEmailAPI/defesa/output"  # Substitua pelo caminho da pasta de saída

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
    doc_list = list_doc(output_dir)
    return doc_list