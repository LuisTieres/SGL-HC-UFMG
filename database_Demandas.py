import pymysql
from PyQt6.QtCore import  QDateTime
import json
import psycopg2
import re
from PyQt6 import QtCore, QtWidgets
from datetime import datetime, date, timedelta

DB_CONFIG = {
    'host': '10.36.0.32',
    'user': 'sglHC2024',
    'password': 'S4g1L81',
    'database': 'sgl'
}

class Ui_data_Demanda(QtWidgets.QMainWindow):

    def ler_historico_por_data(self, tabela, nome=None, prontuario=None, data_nascimento=None, data_filtrada=None,
                               data_inicio=None, data_final=None):
        if not any([nome, prontuario, data_nascimento, data_filtrada]):
            print('[ERRO] Pelo menos um filtro deve ser fornecido.')
            return {}
        print(data_filtrada)
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                condicoes = []
                valores = []

                if nome:
                    condicoes.append("nome = %s")
                    valores.append(nome)

                if prontuario:
                    condicoes.append("prontuario = %s")
                    valores.append(prontuario)

                if data_nascimento:
                    condicoes.append("data_nascimento = %s")
                    valores.append(data_nascimento)

                # Filtro de data dinâmica
                hoje = date.today()
                if data_filtrada == 'HOJE':
                    condicoes.append("data_da_alteracao = %s")
                    valores.append(hoje.strftime('%Y-%m-%d'))
                elif data_filtrada == 'ONTEM':
                    pass
                elif data_filtrada == 'SEMANA':
                    data_semana = hoje - timedelta(days=7)
                    condicoes.append("data_da_alteracao >= %s")
                    valores.append(data_semana)
                    print(data_semana)

                elif data_filtrada == 'MES':
                    data_mes = hoje - timedelta(days=30)
                    condicoes.append("data_da_alteracao >= %s")
                    valores.append(data_mes)

                elif data_filtrada == 'ANO':
                    condicoes.append("YEAR(data_da_alteracao) = %s")
                    valores.append(hoje.year)

                elif data_filtrada == '2ANO':
                    condicoes.append("YEAR(data_da_alteracao) = %s")
                    valores.append(hoje.year - 1)
                    print(valores)

                elif data_filtrada == 'PERSONALIZADO' and data_inicio and data_final:
                    condicoes.append("data_da_alteracao BETWEEN %s AND %s")
                    valores.append(data_inicio)
                    valores.append(data_final)
                print(data_inicio , data_final)
                where_clause = " AND ".join(condicoes) if condicoes else "1"

                query = f"""
                    SELECT DISTINCT alteracao_numero, data_da_alteracao
                    FROM historico_{tabela}
                    WHERE {where_clause}
                    ORDER BY data_da_alteracao ASC, alteracao_numero ASC
                """
                cursor.execute(query, valores)
                versoes = cursor.fetchall()

                if not versoes:
                    print(f'[INFO] Nenhum histórico encontrado com os filtros fornecidos.')
                    return {}

                resultado = {}

                for versao, data in versoes:
                    print(f'[INFO] Carregando data {data}, versão {versao}')

                    filtros_completos = condicoes.copy()
                    valores_completos = valores.copy()

                    filtros_completos.append("alteracao_numero = %s")
                    valores_completos.append(versao)

                    where_completo = " AND ".join(filtros_completos)
                    query_registros = f"""
                        SELECT *
                        FROM historico_{tabela}
                        WHERE {where_completo}
                        LIMIT 1000
                    """

                    cursor.execute(query_registros, valores_completos)
                    registros = cursor.fetchall()

                    resultado[versao] = registros

                return resultado

        except Exception as e:
            print(f'[ERRO] Erro ao ler histórico por data: {e}')
            return {}

        finally:
            if conexao:
                conexao.close()

    def criar_ou_atualizar_snapshot(self, tabela=None, deman=None, pront = str, data_nascimento= str, nome= str,texto= str, nome_da_coluna= str, alteracao_realizada= str):
        try:
            print(tabela, deman, pront , data_nascimento, nome,texto)
            conexao = pymysql.connect(**DB_CONFIG)
            print('teste1')
            with conexao.cursor() as cursor:
                cursor.execute(f"DESCRIBE {tabela}")
                descricao_colunas = cursor.fetchall()
                numero_colunas = len(descricao_colunas)

                print('teste2')


                print('teste4')
                data_atual = datetime.now()
                data = data_atual.strftime('%Y-%m-%d')
                hora = data_atual.strftime('%H:%M:%S')

                print('teste6')
                # Se ainda não há versão, cria uma nova versão
                if deman.numero_versao_atual is None:
                    cursor.execute(f"SELECT MAX(alteracao_numero) FROM historico_{tabela}")
                    resultado = cursor.fetchone()
                    deman.numero_versao_atual = (resultado[0] or 0) + 1
                    print(f'[INFO] Criando nova versão {deman.numero_versao_atual}')

                    cursor.execute(f"SELECT * FROM {tabela}")
                    print('teste8')
                    registros = cursor.fetchall()

                    colunas_dinamicas = ['col'] + [f'col{i}' for i in range(1, numero_colunas)]
                    campos_sql = "alteracao_numero, data_da_alteracao, `h:m:s`, prontuario, nome, data_nascimento, texto,coluna, alteracao, " + ", ".join(
                        colunas_dinamicas)
                    placeholders = ', '.join(['%s'] * (9 + numero_colunas))

                    print('Salvando os nomes das colunas na primeira linha')
                    # Preenche os campos fixos com valores nulos ou identificadores
                    campos_fixos = [deman.numero_versao_atual, data, hora, pront, nome, data_nascimento, texto, nome_da_coluna, alteracao_realizada]
                    valores_colunas = deman.lista_nomes_das_colunas + [''] * (
                                numero_colunas - len(deman.lista_nomes_das_colunas))
                    params = campos_fixos + valores_colunas

                    comando = f"INSERT INTO historico_{tabela} ({campos_sql}) VALUES ({placeholders})"
                    cursor.execute(comando, params)
                    conexao.commit()

                    print('teste7')
                    for registro in registros:
                        print('teste9')
                        campos_fixos = [deman.numero_versao_atual, data, hora, pront, nome, data_nascimento, texto, nome_da_coluna, alteracao_realizada]
                        valores_registro = list(registro)
                        params = campos_fixos + valores_registro

                        cursor.execute(comando, params)
                        conexao.commit()


                else:

                    cursor.execute(f"SELECT id FROM historico_{tabela} WHERE alteracao_numero = %s ORDER BY id",
                                   (deman.numero_versao_atual,))

                    print('teste12')

                    ids_historico = [linha[0] for linha in cursor.fetchall()]

                    cursor.execute(f"SELECT * FROM {tabela}")

                    registros = cursor.fetchall()

                    colunas_dinamicas = ['col'] + [f'col{i}' for i in range(1, numero_colunas)]

                    set_colunas = ', '.join([f"{col} = %s" for col in colunas_dinamicas])

                    comando = f"""

                                UPDATE historico_{tabela}

                                SET data_da_alteracao = %s,

                                    `h:m:s` = %s,

                                    prontuario = %s,

                                    nome = %s,

                                    data_nascimento = %s,

                                    texto = %s,
                                    
                                    coluna = %s,
                                    
                                    alteracao = %s,

                                    {set_colunas}

                                WHERE id = %s

                                """

                    data_atual = datetime.now()

                    data = data_atual.strftime('%Y-%m-%d')

                    hora = data_atual.strftime('%H:%M:%S')

                    # Atualiza o primeiro registro do histórico com os nomes das colunas

                    if len(ids_historico) > 0:
                        id_historico = ids_historico[0]

                        valores_dinamicos = deman.lista_nomes_das_colunas + [''] * (
                                    numero_colunas - len(deman.lista_nomes_das_colunas))

                        params = [data, hora, pront, nome, data_nascimento, texto, nome_da_coluna, alteracao_realizada] + valores_dinamicos + [id_historico]

                        print('[INFO] Atualizando cabeçalho (nomes das colunas):', params)

                        cursor.execute(comando, params)

                        conexao.commit()

                    print('teste15')

                    for idx, registro in enumerate(registros):

                        if idx + 1 >= len(ids_historico):  # +1 para pular o primeiro que já foi atualizado

                            print(f'[AVISO] Não há mais registros no histórico para atualizar.')

                            break

                        id_historico = ids_historico[idx + 1]

                        valores_dinamicos = list(registro)

                        params = [data, hora, pront, nome, data_nascimento, texto, nome_da_coluna, alteracao_realizada] + valores_dinamicos + [id_historico]

                        print(params)

                        cursor.execute(comando, params)

                        print(f'[INFO] Atualizando registro {id_historico} na versão {deman.numero_versao_atual}')

                        conexao.commit()


        except Exception as e:
            print(f'[ERRO] Erro ao criar ou atualizar snapshot: {e}')

        finally:
            if conexao:
                conexao.close()

    def exluir_conta(self,user):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:

                comando = f'DELETE FROM cadastros WHERE user = "{user}"'
                cursor.execute(comando)
                conexao.commit()

            cursor.close()
            conexao.close()

        except Exception as e:
            print(f"Error in ler_btn_tabela_demanda: {e}")
        finally:
            if conexao:
                conexao.close()

    def update_cadastro(self,analise,user,nivelold,nivelnew):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:

                comando = "UPDATE cadastros SET nivel_acesso= %s, analise = %s, novo_nivel_acesso = %s WHERE user = %s"
                valores = (nivelold, analise,nivelnew, user)
                cursor.execute(comando, valores)
                conexao.commit()

            cursor.close()
            conexao.close()

        except Exception as e:
            print(f"Error in ler_btn_tabela_demanda: {e}")
        finally:
            if conexao:
                conexao.close()

    def ler_tipos(self, login):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                lista = []
                cursor.execute("SELECT nome_btn FROM tabelas_deman_names")
                leitura = cursor.fetchall()
                lista.append("NIR")
                for linha in leitura:
                    lista.append(str(linha[0]))
                return lista

        except Exception as e:
            print(f"Error in ler_btn_tabela_demanda: {e}")
        finally:
            if conexao:
                conexao.close()

    def criar_user_(self,login,usuario,name,dialog):

        conexao = pymysql.connect(**DB_CONFIG)
        cursor = conexao.cursor()

        usuario = self.user.text()
        name = self.nome

        comando = f'INSERT INTO cadastros (user,Nome,analise,nivel_acesso) VALUES ("{usuario}","{name}", "0", "{dialog.valor_selecionado}")'
        cursor.execute(comando)
        conexao.commit()

        comando = f'INSERT INTO posicao_usuario_tempo_real (usuario, nome) VALUES ("{usuario}", "{name}")'
        cursor.execute(comando)
        conexao.commit()

        cursor.close()
        conexao.close()

    def ler_cadastros(self,login):
        conexao = pymysql.connect(**DB_CONFIG)

        cursor = conexao.cursor()
        cursor.execute('SELECT user,Nome,analise,nivel_acesso,novo_nivel_acesso FROM cadastros')
        print("Conectado com sucesso")

        leitura = cursor.fetchall()

        return leitura
    def ler_colunas_demanda(self, deman, demanda):
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tabelas_deman_names WHERE id = %s", (demanda,))
            leitura = cursor.fetchall()

            if not leitura:
                print(f"No data found for demanda {demanda}")
                return

            dados = leitura[0]
            dados_filtrados = [valor for valor in dados if valor is not None and valor != '' and valor != 'None']
            contador = 0

            for column, valor in enumerate(dados_filtrados):
                if column > 3:
                    contador += 1
                    deman.quantidade_colunas = contador
                    deman.lista_nomes_das_colunas.append(str(valor))

            self.posicao_antes, self.tabela_antes, self.tipo_antes = (0, 0), '', ''
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Error in ler_colunas_demanda: {e}")

    def ler_btn_tabela_demanda(self, deman):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            deman.lista_btn = []
            with conexao.cursor() as cursor:
                cursor.execute("SELECT nome_btn, nome_tabela, id, ordem FROM tabelas_deman_names")
                leitura = cursor.fetchall()

                for linha in leitura:
                    deman.lista_btn.append(str(linha[0]))
                    deman.lista_titulo.append(str(linha[1]))
                    deman.lista_ids.append(str(linha[2]))
                    deman.lista_ordem_tabelas.append(str(linha[3]))

        except Exception as e:
            print(f"Error in ler_btn_tabela_demanda: {e}")
        finally:
            if conexao:
                conexao.close()

    def atualizar_posicao_tabela(self, deman):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                for cont, id in enumerate(deman.lista_ids):
                    cont+=1
                    comando_update = f'UPDATE tabelas_deman_names SET ordem = %s WHERE id = %s'
                    cursor.execute(comando_update, (cont, id))
                    conexao.commit()

        except Exception as e:
            print(f"Error in ler_btn_tabela_demanda: {e}")
        finally:
            if conexao:
                conexao.close()
    def ler_Widgets_deman(self, deman, demanda):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM tabelas_deman_widgets WHERE id = %s", (demanda,))
                leitura = cursor.fetchall()

                if not leitura:
                    print(f"No widget data for demanda {demanda}")
                    return

                dados = leitura[0]
                for column, valor in enumerate(dados):
                    if column <= deman.quantidade_colunas:
                        deman.lista_widgets.append(str(valor))

        except pymysql.Error as e:
            print('Erro ao conectar ao MySQL:', e)
        finally:
            if conexao:
                conexao.close()

    def validar_nome_tabela(self,tabela):
        if not tabela.isidentifier():
            raise ValueError(f"Invalid table name: {tabela}")

    def modificar_tabela(self, deman, tabela, valor_para_atualizar, id_valor, colum):
        conexao = None
        print('adad', valor_para_atualizar)
        try:
            self.validar_nome_tabela(tabela)
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute(f'SHOW COLUMNS FROM {tabela}')
                colunas = [coluna[0] for coluna in cursor.fetchall()]

                comando_update = f'UPDATE {tabela} SET {colunas[colum]} = %s WHERE {colunas[0]} = %s'
                cursor.execute(comando_update, (valor_para_atualizar, id_valor))

                conexao.commit()

        except Exception as e:
            print(f"Error in modificar_tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    def inserir_na_tabela(self, deman, tabela, valor_para_inserir, id_valor, colum):
        conexao = None
        print('adad', valor_para_inserir)
        try:
            self.validar_nome_tabela(tabela)
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute(f'SHOW COLUMNS FROM {tabela}')
                colunas = [coluna[0] for coluna in cursor.fetchall()]

                comando = f'''
                    INSERT INTO {tabela} (id, {colunas[colum]})
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE {colunas[colum]} = VALUES({colunas[colum]})
                '''
                cursor.execute(comando, (id_valor, valor_para_inserir))

                conexao.commit()
                deman.inserir_linha()

        except Exception as e:
            print(f"Error in inserir_na_tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    def excluir_na_tabela(self, deman, tabela, valores):
        conexao = None
        try:
            self.validar_nome_tabela(tabela)
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                comando = f'DELETE FROM {tabela} WHERE id = %s'
                cursor.executemany(comando, valores)

                conexao.commit()

        except Exception as e:
            print(f"Error in excluir_na_tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    def ler_dabatabase_demandas(self, deman, tabela):
        conexao = None
        try:
            self.validar_nome_tabela(tabela)
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                comando = f'SELECT * FROM {tabela}'
                cursor.execute(comando)
                leitura = cursor.fetchall()
            return leitura

        except Exception as e:
            print(f"Error in ler_dabatabase_demandas: {e}")
            return []
        finally:
            if conexao:
                conexao.close()

    def definir_posicao_usuario(self, tabela, deman, posicao, tipo):
        conexao = None
        try:
            self.validar_nome_tabela(tabela)

            if isinstance(posicao, tuple):
                posicao = f"{posicao[0]},{posicao[1]}"

            if (tabela != self.tabela_antes or
                    posicao != self.posicao_antes or
                    tipo != self.tipo_antes):

                if tabela != self.tabela_antes:
                    posicao = f"{None},{None}"

                self.posicao_antes, self.tabela_antes, self.tipo_antes = posicao, tabela, tipo

                conexao = pymysql.connect(**DB_CONFIG)
                with conexao.cursor() as cursor:
                    cursor.execute(
                        '''
                        UPDATE posicao_usuario_tempo_real 
                        SET posicao = %s, tipo = %s, tabela = %s 
                        WHERE usuario = %s
                        ''',
                        (posicao, tipo, tabela, deman.user)
                    )
                    conexao.commit()

        except Exception as e:
            print(f"Error in definir_posicao_usuario: {e}")
        finally:
            if conexao:
                conexao.close()

    def ler_posicoes_usuarios(self,deman, tipo, tabela):
        conexao = None
        try:
            self.validar_nome_tabela(tabela)
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                comando = '''
                            SELECT usuario, posicao, nome 
                            FROM posicao_usuario_tempo_real
                            WHERE tipo = %s AND tabela = %s
                        '''
                cursor.execute(comando, (tipo, tabela))
                resultados = cursor.fetchall()
            return resultados if resultados else False

        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if conexao:
                conexao.close()

    def enumerar_demanda(self, tabela, deman):
        conexao = None
        try:
            self.validar_nome_tabela(tabela)
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                indice = 1
                for row in range(deman.tabelademan.rowCount()):
                    header_item = deman.tabelademan.verticalHeaderItem(row)
                    if header_item is not None:
                        pac = header_item.text()

                        cursor.execute(
                            f'UPDATE {tabela} SET id = %s WHERE id = %s',
                            (indice, pac)
                        )

                        item = QtWidgets.QTableWidgetItem(str(indice))
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        deman.tabelademan.setVerticalHeaderItem(row, item)

                        indice += 1

                conexao.commit()

        except Exception as e:
            print(f"Error enumerating demanda: {e}")
        finally:
            if conexao:
                conexao.close()

    def salvar_historico(self, deman, lista_modificacao, linha_modificada, linha_antiga, colunas):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            current_datetime = QDateTime.currentDateTime()
            formatted_date = current_datetime.toString('dd/MM/yyyy')

            linha_antiga_str = json.dumps(linha_antiga, ensure_ascii=False)
            linha_modificada_str = json.dumps(linha_modificada, ensure_ascii=False)
            colunas_str = json.dumps(colunas, ensure_ascii=False)

            with conexao.cursor() as cursor:
                for texto in lista_modificacao:
                    comando = '''
                        INSERT INTO history_demandas 
                        (data, histo, tabela_no_momento, tabela_alterada, COLUNAS)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    valores = (
                        formatted_date,
                        texto,
                        linha_antiga_str,
                        linha_modificada_str,
                        colunas_str
                    )
                    cursor.execute(comando, valores)

                conexao.commit()

        except Exception as e:
            print(f"Error saving historico: {e}")
        finally:
            if conexao:
                conexao.close()

    def reservar_leito(self, deman, tabela, status, leito, formatted_datetime, nome,id):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                # Atualiza STATUS SOLICITACAO
                print('status',status)
                column_status = deman.descobrir_nome_coluna('STATUS DA SOLICITAÇÃO', None)
                if column_status is not None:
                    column_status-=1
                    col_name = "col" if column_status == 0 else f"col{column_status}"
                    query = f"UPDATE {tabela} SET {col_name} = %s WHERE id = %s "
                    cursor.execute(query, (status,id,))

                # Atualiza LEITO RESERVADO
                column_leito = deman.descobrir_nome_coluna('LEITO RESERVADO', None)
                if column_leito is not None:
                    column_leito-=1
                    col_name = "col" if column_leito == 0 else f"col{column_leito}"
                    query = f"UPDATE {tabela} SET {col_name} = %s WHERE id = %s "
                    cursor.execute(query, (leito,id,))

                # Atualiza DATA E HORA DA RESERVA
                column_data = deman.descobrir_nome_coluna('DATA E HORA DA RESERVA', None)
                if column_data is not None:
                    column_data -= 1
                    col_name = "col" if column_data == 0 else f"col{column_data}"
                    query = f"UPDATE {tabela} SET {col_name} = %s WHERE id = %s "
                    cursor.execute(query, (formatted_datetime,id,))

                # Atualiza NOME DO PACIENTE
                column_nome = deman.descobrir_nome_coluna('NOME DO PACIENTE', None)
                if column_nome is not None:
                    column_nome -= 1
                    col_name = "col" if column_nome == 0 else f"col{column_nome}"
                    query = f"UPDATE {tabela} SET {col_name} = %s WHERE id = %s "
                    cursor.execute(query, (nome.text(),id,))

            conexao.commit()

        except Exception as e:
            print("Erro ao reservar leito:", e)

        finally:
            if conexao:
                conexao.close()

    def ler_pacientes_aghu(self):
        try:
            with psycopg2.connect(
                    user='ugen_integra',
                    password='aghuintegracao',
                    host='10.36.2.35',
                    port='6544',
                    database='dbaghu'
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
                        SELECT codigo, prontuario, nome, dt_nascimento 
                        FROM agh.aip_pacientes 
                        ORDER BY codigo DESC 
                        LIMIT 2000000
                        '''
                    )
                    rows = cursor.fetchall()
                    return rows

        except psycopg2.Error as e:
            print('Erro ao conectar ao PostgreSQL:', e)
            return []

    def procurar_paciente_mysql(self, deman, coluna, dado, lista_de_Resultados):
        conexao = None
        try:
            if not coluna.isidentifier():
                raise ValueError(f"Invalid column name: {coluna}")

            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cont = 0
                for id in deman.lista_ids:
                    if not id.isidentifier():
                        raise ValueError(f"Invalid table name: {id}")

                    comando = f'''
                        SELECT NOME_DO_PACIENTE, PRONTUARIO, NPF FROM {id}
                        WHERE LOWER({coluna}) LIKE %s
                    '''
                    cursor.execute(comando, (f"%{dado.lower()}%",))

                    resultados = cursor.fetchall()

                    if resultados:
                        lista_de_Resultados.append((resultados, deman.lista_titulo[cont], id))

                    cont += 1

            return lista_de_Resultados if lista_de_Resultados else []

        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            if conexao:
                conexao.close()

    def criar_nova_tabela_demandas(self, deman,tabela, id, table_name, nome_btn):
        if tabela.columnCount() > 5:
            conexao = pymysql.connect(**DB_CONFIG)

            cursor = conexao.cursor()

            headers = []
            for idx in range(len(deman.fixed_columns)):
                if idx == 0:
                    column_field = 'col'
                else:
                    column_field = f'col{idx}'
                headers.append(column_field)
            print(f"Headers sanitizados: {headers}")

            cursor.execute(f"DROP TABLE IF EXISTS {id}")

            columns_sql = ", ".join([f"`{col}` VARCHAR(255)" for col in headers])
            create_table_sql = f"""
                CREATE TABLE {id} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    {columns_sql}
                )
            """
            cursor.execute(create_table_sql)
            print("Tabela criada com sucesso.")
            conexao.commit()
            conexao.close()

            self.atualizar_tabela_names(deman,id,table_name,nome_btn,tabela)

    def atualizar_tabela_names(self, deman, id, table_name, nome_btn, tabela):
        conexao = None
        cursor = None
        try:

            columns = deman.fixed_columns

            conexao = pymysql.connect(**DB_CONFIG)

            cursor = conexao.cursor()

            insert_query = '''
                INSERT INTO tabelas_deman_names (id, nome_tabela, nome_btn, ordem)
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (id, table_name, nome_btn, len(deman.lista_ids)+1))
            conexao.commit()

            for idx, column_name in enumerate(columns):
                if idx == 0:
                    column_field = 'col'
                else:
                    column_field = f'col{idx}'

                update_query = f'''
                    UPDATE tabelas_deman_names
                    SET {column_field} = %s
                    WHERE id = %s
                '''
                cursor.execute(update_query, (column_name, id))

            conexao.commit()

        except Exception as e:
            print(f"Error in atualizar_tabela_names: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

        self.atualizar_tabela_widget(deman, tabela, id)

    def atualizar_tabela_widget(self, deman, tabela, id):
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                insert_query = '''
                    INSERT INTO tabelas_deman_widgets (id)
                    VALUES (%s)
                '''
                cursor.execute(insert_query, (id,))
                for col,value in enumerate(deman.fixed_columns):
                    if col == 0:
                        column_field = 'col'
                    else:
                        column_field = f'col{col}'

                    if value == "DATA DE NASCIMENTO":
                        resposta = 'QDateEdit'

                    elif value == 'DATA E HORA DA RESERVA':
                        resposta = 'QDateTimeEdit'

                    else:
                        resposta = 'QLineEdit'

                    update_query = f'''
                        UPDATE tabelas_deman_widgets
                        SET {column_field} = %s
                        WHERE id = %s
                    '''
                    cursor.execute(update_query, (str(resposta), id))

                conexao.commit()

        except pymysql.MySQLError as e:
            print(f"Erro no banco de dados: {e}")

        finally:
            conexao.close()

    def sanitize_column_name(self, name):
        name = name.strip().lower()
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        if name[0].isdigit():
            name = f'col_{name}'
        return name

    def atualizar_escondidos(self, deman, tabela):
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                todos_ids = set([id_ for (id_, _) in deman.lista_econder] +
                                [id_ for (id_, _) in deman.lista_prioridade_nir])

                for id_valor in todos_ids:

                    from database_Demandas import Ui_data_Demanda
                    self.data_deman = Ui_data_Demanda()
                    hide, priority = self.data_deman.descobrir_escondidos(deman.variavel, id_valor)

                    for (id_, info) in deman.lista_econder:
                        if id_valor == id_:
                            hide = info

                    for (id_, info) in deman.lista_prioridade_nir:
                        if id_valor == id_:
                            priority = info

                    comando = '''
                           INSERT INTO columns_hide_prioridade (id, hide, priority, Tabela)
                           VALUES (%s, %s, %s, %s)
                           ON DUPLICATE KEY UPDATE
                               hide = VALUES(hide),
                               priority = VALUES(priority),
                               Tabela = VALUES(Tabela)
                       '''

                    cursor.execute(comando, (id_valor, hide, priority, tabela))

                conexao.commit()

        except Exception as e:
            print(f"Erro ao atualizar escondidos: {e}")

        finally:
            if conexao:
                conexao.close()

    def descobrir_escondidos(self,deman, tabela, id):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute(
                    "SELECT hide, priority FROM columns_hide_prioridade WHERE tabela = %s AND id = %s",
                    (tabela, id)
                )
                resultado = cursor.fetchone()

                if resultado:
                    hide, priority = resultado
                    return hide, priority
                else:
                    return None, None

        except Exception as e:
            print(f"Erro em descobrir_escondidos: {e}")
            return None, None

        finally:
            if conexao:
                conexao.close()

    def sync_columns(self, tabela, id):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            cursor = conexao.cursor()

            drop_sql = f"""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'sgl' AND TABLE_NAME = '{id}' AND COLUMN_NAME != 'id';
            """

            cursor.execute(drop_sql)
            columns = [row[0] for row in cursor.fetchall()]

            for col in columns:
                sql = f"ALTER TABLE {id} DROP COLUMN {col};"
                cursor.execute(sql)

            # 🔥 Step 2: Add columns based on PyQt table
            col_count = tabela.columnCount() - 1

            for i in range(col_count):
                if i == 0:
                    col_name = "col"
                else:
                    col_name = f"col{i}"
                sql = f"ALTER TABLE {id} ADD COLUMN {col_name} VARCHAR(255);"
                cursor.execute(sql)

            conexao.commit()
            conexao.close()

        except Exception as e:
            print("Error", str(e))

    def upload_table_to_database(self, tabela, tabela_name, deman):
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                row_count = deman.tabelademan.rowCount()
                col_count = len(deman.ordem_colunas)

                for row in range(row_count):
                    header_item = deman.tabelademan.verticalHeaderItem(row)
                    if header_item is None:
                        continue
                    if header_item.text() == '':
                        continue
                    if header_item.text() != f'{row + 1}':
                        continue

                    for idx, col in enumerate(deman.ordem_colunas):
                        column_name = "col" if col == 0 else f"col{col}"
                        item = tabela.item(row, int(col + 1))
                        print(col, column_name, idx, 'analisepea')

                        if item is None:
                            value = None
                        else:
                            value = item.text()

                        sql = f"""
                                                    UPDATE {tabela_name}
                                                    SET {column_name} = %s
                                                    WHERE id = %s
                                                """
                        cursor.execute(sql, (value, row + 1))

                conexao.commit()
                print(f"Data uploaded successfully to '{tabela_name}'.")

        except Exception as e:
            print(f"Database upload error: {e}")

    def update_button_position_in_db(self,button_name, position):
        conexao = pymysql.connect(**DB_CONFIG)

        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM buttons_table WHERE name = %s", (button_name,))
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute(
                "INSERT INTO buttons_table (name, position) VALUES (%s, %s)",
                (button_name, position)
            )
        else:
            cursor.execute(
                "UPDATE buttons_table SET position = %s WHERE name = %s",
                (position, button_name)
            )

        conexao.commit()
        conexao.close()

    def excluir_tabela_mysql(self, deman, tabela_id):
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            cursor = conexao.cursor()

            # Drop the MySQL table
            sql = f"DROP TABLE IF EXISTS `{tabela_id}`"
            cursor.execute(sql)

            # Delete from control tables by ID
            comando1 = 'DELETE FROM tabelas_deman_names WHERE id = %s'
            cursor.execute(comando1, (tabela_id,))

            comando2 = 'DELETE FROM tabelas_deman_widgets WHERE id = %s'
            cursor.execute(comando2, (tabela_id,))

            conexao.commit()

            print(f"Table '{tabela_id}' and related records were deleted successfully.")

        except Exception as e:
            print(f"Error while dropping table: {e}")

        finally:
            cursor.close()
            conexao.close()

    def ler_ultimo_id_tabela_mysql(self, demanda, tabela):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {tabela} ORDER BY id DESC LIMIT 1")
                resultado = cursor.fetchone()
                return resultado[0] if resultado else None

        except Exception as e:
            print(f"Erro ao ler o último ID da tabela '{tabela}': {e}")
            return None
        finally:
            if conexao:
                conexao.close()

    def add_columns(self, deman, new_order, old_order, TABLE_NAME):
        conexao = pymysql.connect(**DB_CONFIG)
        with conexao.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {TABLE_NAME}")
            existing_cols = [row[0] for row in cursor.fetchall()]
            print(existing_cols)
            quantidade = len(new_order) - len(old_order)

            if len(old_order) == 0:
                last_num = 0
            else:
                # Pega o número da última coluna
                last_str = old_order[-1]
                last_num = int(''.join(filter(str.isdigit, last_str))) if any(
                    char.isdigit() for char in last_str) else 0

            for _ in range(quantidade):
                while True:
                    new_col = 'col' if last_num == 0 else f'col{last_num}'
                    if new_col not in existing_cols:
                        break
                    last_num += 1

                print(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {new_col} TEXT")
                cursor.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN {new_col} TEXT")
                existing_cols.append(new_col)
                last_num += 1

        conexao.commit()

        conexao.close()

    def alterar_ordem_tabela(self,deman, tabela, new_order, old_order):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            deman.lista_btn = []
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {tabela}")
                leitura = cursor.fetchall()
                print(f"Lendo tabela {tabela} com {len(leitura)} linhas.")

                for linha in leitura:
                    print(f"Linha: {linha}")

                    def extrair_indice_coluna(nome):
                        if nome == 'col':
                            return 0
                        match = re.search(r'\d+', nome)
                        return int(match.group()) if match else None

                    for column, valor in enumerate(linha):
                        if column == 0:
                            continue

                        column_field = 'col' if column == 1 else f'col{column - 1}'

                        index = column - 1
                        new_val = new_order[index] if index < len(new_order) else None
                        old_val = old_order[index] if index < len(old_order) else None

                        if new_val != old_val:
                            indice_valor = extrair_indice_coluna(new_val)
                            if indice_valor is not None and indice_valor + 1 < len(linha):
                                valor = linha[indice_valor + 1]
                            print(f"Alterando valor na coluna '{column_field}' para linha ID {linha[0]} valor {valor}")
                            cursor.execute(
                                f"UPDATE {tabela} SET {column_field} = %s WHERE id = %s",
                                (valor, linha[0])
                            )

                for column, valor in enumerate(new_order):
                    if column == 0:
                        column_field = 'col'
                    else:
                        column_field = f'col{column}'

                    old_val = old_order[column] if column < len(old_order) else None

                    if valor != old_val:
                        widget_info = deman.widgets_colunas.get(valor)
                        nome = deman.nomes_colunas.get(valor)

                        if isinstance(widget_info, list):
                            widget_info = json.dumps(widget_info)

                        if isinstance(nome, list):
                            nome = json.dumps(nome)

                        print(f"Atualizando coluna {column_field} com valor {widget_info} para id {tabela}")
                        cursor.execute(
                            f"UPDATE tabelas_deman_widgets SET {column_field} = %s WHERE id = %s",
                            (widget_info, tabela)
                        )

                        print(f"Atualizando coluna {column_field} com valor {nome} para id {tabela}")
                        cursor.execute(
                            f"UPDATE tabelas_deman_names SET {column_field} = %s WHERE id = %s",
                            (nome, tabela)
                        )

                conexao.commit()
        except Exception as e:
            print(f"Error in alterar_ordem_tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    def alterar_widget_name(self, deman, tabela, new_order, old_order):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            deman.lista_btn = []
            with conexao.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {tabela}")
                leitura = cursor.fetchall()
                print(f"Lendo tabela {tabela} com {len(leitura)} linhas.")

                for column, valor in enumerate(new_order):
                    if column == 0:
                        column_field = 'col'
                    else:
                        column_field = f'col{column}'

                    old_val = old_order[column] if column < len(old_order) else None


                    widget_info = deman.widgets_colunas.get(valor)
                    nome = deman.nomes_colunas.get(valor)

                    if isinstance(widget_info, list):
                        widget_info = json.dumps(widget_info)

                    if isinstance(nome, list):
                        nome = json.dumps(nome)

                    print(f"Atualizando coluna {column_field} com valor {widget_info} para id {tabela}")
                    cursor.execute(
                        f"UPDATE tabelas_deman_widgets SET {column_field} = %s WHERE id = %s",
                        (widget_info, tabela)
                    )
                    print(f"Atualizando coluna {column_field} com valor {nome} para id {tabela}")
                    cursor.execute(
                        f"UPDATE tabelas_deman_names SET {column_field} = %s WHERE id = %s",
                        (nome, tabela)
                    )

                conexao.commit()
        except Exception as e:
            print(f"Error in alterar_widget_name: {e}")
        finally:
            if conexao:
                conexao.close()

    def deletar_coluna(self, deman, tabela, coluna):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                comando = f"ALTER TABLE {tabela} DROP COLUMN {coluna}"
                cursor.execute(comando)
                cursor.execute(
                    f"UPDATE tabelas_deman_widgets SET {coluna} = '' WHERE id = %s",
                    (tabela,)
                )
                cursor.execute(
                    f"UPDATE tabelas_deman_names SET {coluna} = '' WHERE id = %s",
                    (tabela,)
                )
                conexao.commit()
                print(f"Coluna {coluna} deletada com sucesso da tabela {tabela}")

        except Exception as e:
            print(f"Erro ao deletar coluna: {e}")
        finally:
            if conexao:
                conexao.close()
    def pegar_coluna_Demanda(self, grade, id, coluna_name):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tabelas_deman_names WHERE id = %s", (id,))
            leitura = cursor.fetchall()

            if not leitura:
                print(f"No data found for grade {id}")
                return

            dados = leitura[0]
            dados_filtrados = [valor for valor in dados if valor is not None]

            for column, valor in enumerate(dados_filtrados):
                if column > 3:

                    if coluna_name == str(valor):
                        return column - 4

            cursor.close()
            conexao.close()
            return None
        except Exception as e:
            print(f"Error in ler_colunas_grade: {e}")

    def pegar_Dados_Demanda(self, demanda, tabela, column):
        conexao = pymysql.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        comando = f'SELECT {column} FROM {tabela}'
        cursor.execute(comando)
        resultados = cursor.fetchall()
        conexao.close()

        # Evita erro mesmo se houver linhas com valor None
        return [linha[0] for linha in resultados if linha[0] is not None]

