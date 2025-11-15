from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMessageBox

from PyQt6 import QtCore, QtGui, QtWidgets
from ldap3 import Server, Connection, ALL, SUBTREE
import ast
import sys
import os
def resource_path(relative_path):
    """Resolve path para PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


variaveis = {
    "AUTH_LDAP_SERVER_URI": "ldap://10.36.2.21",
    "AUTH_LDAP_BIND_DN": "CN=TAGS,OU=Servicos,OU=Usuarios,OU=HCMG,OU=EBSERH,DC=ebserhnet,DC=ebserh,DC=gov,DC=br",
    "AUTH_LDAP_BIND_PASSWORD": "T4g5@2022!",
    "AUTH_LDAP_BASE_DN": "OU=Usuarios,OU=HCMG,OU=EBSERH,DC=ebserhnet,DC=ebserh,DC=gov,DC=br"
}
class Ui_API(QtWidgets.QMainWindow):
    def buscar_usuario(self, username: str):
        server = Server(variaveis["AUTH_LDAP_SERVER_URI"], get_info=ALL)
        conn = Connection(
            server,
            user=variaveis["AUTH_LDAP_BIND_DN"],
            password=variaveis["AUTH_LDAP_BIND_PASSWORD"],
            auto_bind=True,
        )

        filtro = f"(samaccountname={username})"
        conn.search(
            search_base=variaveis["AUTH_LDAP_BASE_DN"],
            search_filter=filtro,
            search_scope=SUBTREE,
            attributes=["distinguishedName", "displayName", "mail", "title", "department", "thumbnailPhoto"]
        )

        if conn.entries:
            entry = conn.entries[0]
            foto_binario = entry.thumbnailPhoto.value

            caminho_imagem = None
            if foto_binario:
                # Caminho da pasta Imagens do usuário
                pasta_imagens = Path(expanduser("~")) / "Pictures"
                pasta_imagens.mkdir(parents=True, exist_ok=True)

                caminho_imagem = pasta_imagens / f"imagem_do_usuario_{username}.png"
                with open(caminho_imagem, 'wb') as f:
                    f.write(foto_binario)

            dados = {
                "dn": entry.entry_dn,
                "nome": entry.displayName.value,
                "email": entry.mail.value,
                "cargo": entry.title.value,
                "departamento": entry.department.value,
                "caminho_imagem": str(caminho_imagem) if caminho_imagem else None
            }
            conn.unbind()
            return dados

        conn.unbind()
        return None

    def senha_correta(self,user_dn: str, senha: str) -> bool:
        server = Server(variaveis["AUTH_LDAP_SERVER_URI"], get_info=ALL)
        try:
            conn = Connection(server, user=user_dn, password=senha, auto_bind=True)
            conn.unbind()
            return True
        except Exception:
            return False

    def verificar_usuario_senha(self,username: str, senha: str):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("AVISO")
        usuario = self.buscar_usuario(username)
        if not usuario:
            msg_box.setText("❌ Usuário NÃO existe no AD.")

            icon = QtGui.QIcon(resource_path('imagens/escondido.png'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            return False
        elif self.senha_correta(usuario["dn"], senha):

            self.nome =usuario['nome']
            self.email = usuario['email']
            self.cargo = usuario['cargo']
            self.departamento = usuario['departamento']

            print(f"👤 Nome: {usuario['nome']}")
            print(f"📧 Email: {usuario['email']}")
            print(f"💼 Cargo: {usuario['cargo']}")
            print(f"🏢 Departamento: {usuario['departamento']}")

            return True
        else:
            msg_box.setText("❌ Usuário existe, mas a senha está INCORRETA.")

            icon = QtGui.QIcon(resource_path('imagens/escondido.png'))
            msg_box.setWindowIcon(icon)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply = msg_box.exec()
            return False