import os

def converter_txt_para_py():
    diretorio_atual = os.getcwd()
    
    for filename in os.listdir(diretorio_atual):
        if filename.endswith(".txt"):
            caminho_antigo = os.path.join(diretorio_atual, filename)
            novo_nome = filename.replace(".txt", ".py")
            caminho_novo = os.path.join(diretorio_atual, novo_nome)
            
            os.rename(caminho_antigo, caminho_novo)
            print(f"Arquivo {filename} convertido para {novo_nome}.")

converter_txt_para_py()
