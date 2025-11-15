from PyQt6 import QtWidgets
import sys
import os
import subprocess
import shutil
import winshell
from win32com.client import Dispatch
import time
from Login import Ui_Form

CAMINHO_REDE = r"\\10.36.0.44\Grupos2\Sistemas-USID\Sistema de Gestão de Leitos NIR"
NOME_EXE = "Gestão de Leitos.exe"
PASTA_LOCAL = r"C:\SistemaNIR"

def obter_data_modificacao(path_file):
    return os.path.getmtime(path_file) if os.path.exists(path_file) else 0

def criar_atalho(exe_path):
    desktop = winshell.desktop()
    caminho_atalho = os.path.join(desktop, "Gestão de Leitos.lnk")

    shell = Dispatch('WScript.Shell')
    atalho = shell.CreateShortCut(caminho_atalho)
    atalho.Targetpath = str(exe_path)
    atalho.WorkingDirectory = os.path.dirname(exe_path)
    atalho.IconLocation = str(exe_path)
    atalho.save()
    print(f"Atalho criado ou atualizado em: {caminho_atalho}")

def atualizar_exe():
    exe_rede = os.path.join(CAMINHO_REDE, NOME_EXE)
    exe_local = os.path.join(PASTA_LOCAL, NOME_EXE)

    if not os.path.exists(exe_rede):
        print("EXE na rede não encontrado.")
        if not os.path.exists(exe_local):
            print("EXE também não existe localmente. Não é possível continuar.")
            input("Pressione ENTER para sair...")
            sys.exit(1)
        else:
            print("Iniciando versão local que já existe.")
            iniciar_interface_login()
            return

    os.makedirs(PASTA_LOCAL, exist_ok=True)

    data_rede = obter_data_modificacao(exe_rede)
    data_local = obter_data_modificacao(exe_local)

    print(f"Data de modificação - Local: {time.ctime(data_local)} | Rede: {time.ctime(data_rede)}")

    if data_rede > data_local:
        print("Nova versão encontrada! Atualizando...")
        shutil.copy2(exe_rede, exe_local)
        print(f"EXE atualizado em: {exe_local}")
        criar_atalho(exe_local)
        print("Executando o EXE atualizado...")
        subprocess.Popen([exe_local])
        sys.exit(0)
    else:
        print("Já está na versão mais recente.")
        iniciar_interface_login()

def iniciar_interface_login():
    app = QtWidgets.QApplication(sys.argv)
    janela_login = QtWidgets.QMainWindow()
    login = Ui_Form()
    login.setupUi(janela_login)
    janela_login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    atualizar_exe()
