import mysql.connector
from mysql.connector import Error

def apagar_coluna(host, user, password, database, tabela, coluna):
    try:
        # Conexão com o banco de dados
        conexao = mysql.connector.connect(host='10.36.0.32', user='sglHC2024', password='S4g1L81', database='sgl')
        if conexao.is_connected():
            print(f"Conectado ao banco de dados {database}")

            # Cursor para executar comandos SQL
            cursor = conexao.cursor()

            # Comando SQL para apagar a coluna
            comando_sql = f"""
            ALTER TABLE `{tabela}`
            DROP COLUMN `{coluna}`;
            """
            cursor.execute(comando_sql)
            conexao.commit()
            print(f"Coluna `{coluna}` removida com sucesso da tabela `{tabela}`.")

    except Error as e:
        print(f"Erro ao conectar ou apagar coluna: {e}")

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

# Exemplo de uso
apagar_coluna(
    host="10.36.133.117",
    user="sglHC2024",
    password="sua_senha",
    database="sgl",
    tabela="tabela_agenda_bloco_demanda",
    coluna="data_demanda"
)
