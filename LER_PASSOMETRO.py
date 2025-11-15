import mysql.connector

# Conectar ao banco de dados
conexao = mysql.connector.connect(
    host='10.36.0.32',
    user='sglHC2024',
    password='S4g1L81',
    database='sgl'
)

cursor = conexao.cursor()

# Definir o valor do usuário e o novo departamento
usuario = '48'  # Substitua pelo nome do usuário desejadofifinueva41
novo_departamento = '01/01/2000 00:00'  # Substitua pelo novo valor de departamento

# SQL para atualizar a coluna 'departamento' com base no 'user'
sql = """
    UPDATE tabela_demanda_ps
    SET data_demanda = %s
    WHERE idtabela_demanda_ps = %s
"""

# Executar a consulta
cursor.execute(sql, (novo_departamento, usuario))

# Confirmar a transação
conexao.commit()

# Verificar se a atualização foi bem-sucedida
if cursor.rowcount > 0:
    print(f'Departamento do usuário {usuario} alterado para {novo_departamento}.')
else:
    print(f'Usuário {usuario} não encontrado.')

# Fechar a conexão
cursor.close()
conexao.close()
