import pymysql
import json

# Dados de conexão
conexao = pymysql.connect(
    host='10.36.0.32',
    user='sglHC2024',
    password='S4g1L81',
    database='sgl'
)

# Sua lista de especialidades
especialidades = [
    'ENFERMARIA FEMININA',
    'ENFERMARIA MASCULINA',
    'PEDIÁTRICO',
    'CTI ADULT/UCO',
    'CTI NEONATOLOGIA',
    'CTI PEDIÁTRICO',
    'ISOLAMENTO CONTATO',
    'ISOLAMENTO RESPIRATÓRIO',
    'MATERNIDADE',
    'APARTAMENTO',
    'ENFERMARIA COVID',
    'CTI COVID',
    'INTERNAÇÃO VIRTUAL'
]

# Converte para JSON
especialidades_json = json.dumps(especialidades, ensure_ascii=False)

try:
    with conexao.cursor() as cursor:
        # Exemplo: atualizar o registro com id=1
        sql = "UPDATE tabelas_deman_Widgets SET col10 = %s WHERE id = %s"
        cursor.execute(sql, (especialidades_json, 'tabela_agenda_bloco_demanda'))
        conexao.commit()
        print("Atualização realizada com sucesso!")

except Exception as e:
    print("Erro:", e)

finally:
    conexao.close()
