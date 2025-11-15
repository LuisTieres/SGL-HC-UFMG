import pymysql
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QStyledItemDelegate, QLineEdit,QMessageBox
from PyQt6.QtCore import  Qt,QDateTime
import json
import psycopg2
import re
from PyQt6 import QtCore, QtGui, QtWidgets
from datetime import datetime, date, timedelta
import os
import re
import pymysql
from openpyxl import Workbook  # pode remover se não for mais salvar em Excel
from PyQt6.QtCore import QDateTime
from datetime import datetime, timedelta
DB_CONFIG = {
    'host': '10.36.0.32',
    'user': 'sglHC2024',
    'password': 'S4g1L81',
    'database': 'sgl'
}
class Ui_data_Grade(QtWidgets.QMainWindow):

    def atualizar_senso(self,grade):
        analise = True
        data_atual = QDateTime.currentDateTime()
        dia = data_atual.date().day()
        mes = data_atual.date().month()
        ano = data_atual.date().year()
        dia = int(dia) - 1
        data_ontem = datetime(ano, mes, dia).date()

        # Verificar se já existe no banco
        conexao = pymysql.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM senso_diario WHERE data = %s LIMIT 1", (data_ontem,))
        resultado = cursor.fetchone()

        if resultado:
            print("Já existe entrada para o dia", data_ontem)
            return  # já tem dados para esse dia

        # Caso não tenha, coletar dados e inserir
        rows = ['', 'PS|UDC - AGHU', 'PS|CORREDOR - AGHU', 'PS|PEDIATRIA - AGHU', 'PS|UTI - AGHU',
                '2º LESTE - GRADE', '2º SUL - GRADE', '3º LESTE/CTI - GRADE', '3º NORTE/UCO - GRADE',
                'MÃE CANGURU - CENSO EBSERH', 'PRÉ-PARTO - CENSO EBSERH', 'MATERNIDADE - CENSO EBSERH',
                'NEO (UTIN/UCIN) - CENSO EBSERH', '6º LESTE - GRADE', '6º NORTE/CTI PEDIATRICO - GRADE',
                '7º LESTE - GRADE', '7º NORTE - GRADE', '8º LESTE - GRADE', '8º NORTE - GRADE',
                '8º SUL - GRADE', '9º LESTE - GRADE', '10º NORTE - GRADE', 'HOSPITAL SÃO GERALDO - AGHU',
                'CLÍNICO ADULTO', 'CIRÚRGICO ADULTO', 'OBSTÉTRICO', 'PEDIATRICO', 'CTI - ADULTO', 'CTI - PEDIATRICO']

        ocupado_total = 0
        bloqueado_total = 0
        total_leitos = 0

        for row in range(1, len(rows)):
            grade.total = 0
            grade.ocupado_senso = 0
            grade.bloqueado_senso = 0
            ala = rows[row]
            grade.dados_senso(ala)

            # Calcular dados
            ocupados = grade.ocupado_senso
            bloqueados = grade.bloqueado_senso
            leitos = grade.total

            leitos_disponiveis = leitos - bloqueados
            if leitos_disponiveis > 0:
                percentual_ocupacao = ocupados / leitos_disponiveis * 100
            else:
                percentual_ocupacao = 0.0

            ocupado_total += ocupados
            bloqueado_total += bloqueados
            total_leitos += leitos

            # Inserir no banco
            cursor.execute("""
                INSERT INTO senso_diario (data, ala, ocupacao, bloqueios, cnes, ocupacao_percentual, leitos_disponiveis)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                data_ontem,
                ala,
                ocupados,
                bloqueados,
                leitos,
                round(percentual_ocupacao, 2),
                leitos_disponiveis
            ))

        conexao.commit()
        cursor.close()
        conexao.close()
        print("Dados inseridos no banco para o dia", data_ontem)

    def criar_ou_atualizar_snapshot(self, tabela=None, deman=None, pront=str, data_nascimento=str, nome=str, texto=str,
                                    nome_da_coluna=str, alteracao_realizada=str,leitura=list):
        try:
            print(tabela, deman, pront, data_nascimento, nome, texto)
            conexao = pymysql.connect(**DB_CONFIG)
            print('teste1')
            with conexao.cursor() as cursor:
                cursor.execute(f"DESCRIBE grade")
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

                    cursor.execute(f"SELECT * FROM grade")
                    print('teste8')
                    registros = leitura

                    colunas_dinamicas = ['col'] + [f'col{i}' for i in range(1, numero_colunas)]
                    campos_sql = "alteracao_numero, data_da_alteracao, `h:m:s`, prontuario, nome, data_nascimento, texto,coluna, alteracao, " + ", ".join(
                        colunas_dinamicas)
                    placeholders = ', '.join(['%s'] * (9 + numero_colunas))

                    print('Salvando os nomes das colunas na primeira linha')
                    # Preenche os campos fixos com valores nulos ou identificadores
                    campos_fixos = [deman.numero_versao_atual, data, hora, pront, nome, data_nascimento, texto,
                                    nome_da_coluna, alteracao_realizada]
                    valores_colunas = deman.lista_nomes_das_colunas + [''] * (
                            numero_colunas - len(deman.lista_nomes_das_colunas))
                    params = campos_fixos + valores_colunas

                    comando = f"INSERT INTO historico_{tabela} ({campos_sql}) VALUES ({placeholders})"
                    cursor.execute(comando, params)
                    conexao.commit()

                    print('teste7')
                    for registro in registros:
                        print('teste9')
                        campos_fixos = [deman.numero_versao_atual, data, hora, pront, nome, data_nascimento, texto,
                                        nome_da_coluna, alteracao_realizada]
                        valores_registro = list(registro)
                        params = campos_fixos + valores_registro

                        cursor.execute(comando, params)
                        conexao.commit()


                else:

                    cursor.execute(f"SELECT id FROM historico_{tabela} WHERE alteracao_numero = %s ORDER BY id",
                                   (deman.numero_versao_atual,))

                    print('teste12')

                    ids_historico = [linha[0] for linha in cursor.fetchall()]

                    cursor.execute(f"SELECT * FROM grade")

                    registros = leitura

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

                        params = [data, hora, pront, nome, data_nascimento, texto, nome_da_coluna,
                                  alteracao_realizada] + valores_dinamicos + [id_historico]

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

                        params = [data, hora, pront, nome, data_nascimento, texto, nome_da_coluna,
                                  alteracao_realizada] + valores_dinamicos + [id_historico]

                        print(params)

                        cursor.execute(comando, params)

                        print(f'[INFO] Atualizando registro {id_historico} na versão {deman.numero_versao_atual}')

                        conexao.commit()


        except Exception as e:
            print(f'[ERRO] Erro ao criar ou atualizar snapshot: {e}')

        finally:
            if conexao:
                conexao.close()

    def ler_colunas_Grade(self, grade, idGRADE):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tabelas_grade_names WHERE id = %s", (idGRADE,))
            leitura = cursor.fetchall()

            if not leitura:
                print(f"No data found for grade {idGRADE}")
                return

            dados = leitura[0]
            dados_filtrados = [valor for valor in dados if valor is not None]
            contador = 0

            for column, valor in enumerate(dados_filtrados):
                if column > 2:
                    contador += 1
                    grade.quantidade_colunas = contador
                    grade.lista_nomes_das_colunas.append(str(valor))

            self.posicao_antes, self.tabela_antes, self.tipo_antes = (0, 0), '', ''
            cursor.close()
            conexao.close()
        except Exception as e:
            print(f"Error in ler_colunas_grade: {e}")
    def definir_posicao_usuario(self, tabela, deman, posicao, tipo):
        conexao = None
        try:
            print('postion ', posicao)
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

                    print('postion2 ', posicao)
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
    def ler_btn_tabela_Grade(self, grade):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            grade.lista_btn = []
            with conexao.cursor() as cursor:
                cursor.execute("SELECT nome_btn, nome_tabela, id FROM tabelas_grade_names")
                leitura = cursor.fetchall()

                for linha in leitura:
                    grade.lista_btn.append(str(linha[0]))
                    grade.lista_titulo.append(str(linha[1]))
                    grade.lista_ids.append(str(linha[2]))

        except Exception as e:
            print(f"Error in ler_btn_tabela_Grade: {e}")
        finally:
            if conexao:
                conexao.close()

    def ler_Widgets_Grade(self, grade, idGRADE):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM tabelas_grade_widgets WHERE id = %s", (idGRADE,))
                leitura = cursor.fetchall()

                if not leitura:
                    print(f"No widget data for grade {idGRADE}")
                    return

                dados = leitura[0]
                for column, valor in enumerate(dados):
                    if column <= grade.quantidade_colunas:
                        grade.lista_widgets.append(str(valor))

        except pymysql.Error as e:
            print('Erro ao conectar ao MySQL:', e)
        finally:
            if conexao:
                conexao.close()
    def validar_nome_tabela(self,tabela):
        if not tabela.isidentifier():
            raise ValueError(f"Invalid table name: {tabela}")

    def modificar_tabela(self, grade, valor_para_atualizar, id_valor, colum):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            with conexao.cursor() as cursor:
                cursor.execute(f'SHOW COLUMNS FROM grade')
                colunas = [coluna[0] for coluna in cursor.fetchall()]
                LEITOS = id_valor.replace(' ', '_')
                comando_update = f'UPDATE grade SET {colunas[colum]} = %s WHERE idGRADE = %s'
                cursor.execute(comando_update, (valor_para_atualizar, LEITOS))

                conexao.commit()

        except Exception as e:
            print(f"Error in modificar_tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    def retirar_aguardando(self, i, grade):
        try:
            item = grade.tabela_grade.verticalHeaderItem(i + 1)
            if item is not None and 'aguardando' in item.text():
                print(item.text(), 'leito aguarda')

                try:
                    conexao = pymysql.connect(**DB_CONFIG)
                    cursor = conexao.cursor()

                    leito = grade.tabela_grade.verticalHeaderItem(i)
                    if leito is None:
                        raise ValueError("Leito não encontrado no índice especificado.")

                    leito_text = leito.text().replace(' ', '_')

                    comando1 = f'DELETE FROM grade WHERE idGRADE = "{leito_text}"'
                    comando2 = f'UPDATE grade SET idGRADE = "{leito_text}" WHERE idGRADE = "{leito_text}_aguardando"'

                    cursor.execute(comando1)
                    conexao.commit()

                    cursor.execute(comando2)
                    conexao.commit()

                except pymysql.MySQLError as erro_mysql:
                    print("Erro MySQL:", erro_mysql)
                    QMessageBox.critical(None, "Erro no Banco de Dados", f"Ocorreu um erro MySQL:\n{erro_mysql}")

                except Exception as erro:
                    print("Erro geral:", erro)
                    QMessageBox.critical(None, "Erro", f"Ocorreu um erro:\n{erro}")

                finally:
                    try:
                        if cursor:
                            cursor.close()
                        if conexao:
                            conexao.close()
                    except:
                        pass

        except Exception as erro_geral:
            print("Erro ao acessar a grade:", erro_geral)
            QMessageBox.critical(None, "Erro", f"Erro ao acessar a grade:\n{erro_geral}")
    def lista_leitos_filtro_aghu(self,grade):
        lista_leitos = []
        connection = psycopg2.connect(user='ugen_integra', password='aghuintegracao', host='10.36.2.35', port='6544',
                                      database='dbaghu')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT lto_id, leito FROM AGH.ain_leitos WHERE unf_seq = %s AND ind_situacao != %s",
            (grade.codigo_ala, 'I')
        )

        rows = cursor.fetchall()
        for row in rows:
            sem_hifen = row[0].split('-')[0]
            semzero = row[1].lstrip('0')
            dados = f'{sem_hifen}_{semzero}'
            lista_leitos.append(dados)
            dados = dados + '_aguardando'
            lista_leitos.append(dados)
        return lista_leitos
    def ler_database(self,grade,lista_leitos):
        conexao = pymysql.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        leitos_str = ', '.join([f'\"{leito}\"' for leito in lista_leitos])
        comando = f'SELECT * FROM grade WHERE idGRADE IN ({leitos_str})'
        cursor.execute(comando)
        return cursor.fetchall()

    def reservar_leito_grade_reserva(self,reserva, tipo, obs, pronto, npf, nome, status, data_nas, leito, idGRADE,
                                     formatted_datetime):
        try:
            conexao = pymysql.connect(**DB_CONFIG)

            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM tabelas_grade_names WHERE id = %s", (idGRADE,))
                leitura = cursor.fetchone()

                if not leitura:
                    print(f"Nenhum dado encontrado para grade {idGRADE}")
                    return

                nome_tabela = reserva.labeltitulo.text()
                updates = {}
                for idx, valor in enumerate(leitura[3:], start=3):  # pula id, outro campo e começa no 3
                    coluna_bd = "col" if idx - 3 == 0 else f"col{idx - 3}"

                    print(str(valor), coluna_bd, 'analise reserva')
                    match str(valor).strip().upper():
                        case "SEXO DA ENFERMARIA":
                            updates[coluna_bd] = tipo
                        case "OBSERVACOES":
                            updates[coluna_bd] = obs
                        case "PRONTUÁRIO":
                            updates[coluna_bd] = pronto
                        case "NPF":
                            updates[coluna_bd] = npf
                        case "NOME DO PACIENTE":
                            updates[coluna_bd] = nome.text() if hasattr(nome, 'text') else nome
                        case "STATUS DO LEITO":
                            updates[coluna_bd] = status
                        case "DATA DE NASCIMENTO":
                            updates[coluna_bd] = data_nas.text() if hasattr(data_nas, 'text') else data_nas
                        case "DATA E HORA DE ATUALIZAÇÃO DO STATUS":
                            updates[coluna_bd] = formatted_datetime
                        case "SOLICITANTE":
                            updates[coluna_bd] = nome_tabela

                if not updates:
                    print("Nenhum dado para atualizar.")
                    return

                set_clause = ", ".join(f"{col} = %s" for col in updates.keys())
                valores = list(updates.values())

                cursor.execute("SELECT 1 FROM grade WHERE idGRADE = %s", (leito,))
                existe = cursor.fetchone()

                if not existe:
                    cursor.execute("INSERT INTO grade (idGRADE) VALUES (%s)", (leito,))
                    print(f"Leito {leito} inserido.")

                sql = f"UPDATE grade SET {set_clause} WHERE idGRADE = %s"
                valores.append(leito)

                cursor.execute(sql, valores)
                conexao.commit()
                print("Atualização realizada com sucesso.")


        except Exception as e:
            print(f"Erro na função reservar_leito_grade_reserva: {e}")
    def pegar_coluna_Grade(self, grade, idGRADE, coluna_name):
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tabelas_grade_names WHERE id = %s", (idGRADE,))
            leitura = cursor.fetchall()

            if not leitura:
                print(f"No data found for grade {idGRADE}")
                return

            dados = leitura[0]
            dados_filtrados = [valor for valor in dados if valor is not None]

            for column, valor in enumerate(dados_filtrados):
                if column > 2:

                    if coluna_name == str(valor):
                        return column - 3

            cursor.close()
            conexao.close()
            return None
        except Exception as e:
            print(f"Error in ler_colunas_grade: {e}")

    def pegar_Dados_Grade(self, grade, leito, column):
        conexao = pymysql.connect(**DB_CONFIG)
        leito_text = leito.replace(' ', '_')
        print(leito_text)
        cursor = conexao.cursor()
        comando = f'SELECT {column} FROM grade WHERE idGRADE = %s'
        cursor.execute(comando, (leito_text,))
        resultado = cursor.fetchone()
        conexao.close()
        return resultado[0] if resultado else None

    def pegar_Dados_das_Colunas_Grade(self, grade, colunas):
        conexao = pymysql.connect(**DB_CONFIG)
        cursor = conexao.cursor()
        colunas_str = ", ".join(colunas)
        comando = f'SELECT {colunas_str} FROM grade'

        cursor.execute(comando)
        dados = cursor.fetchall()

        cursor.close()
        conexao.close()

        return dados

    def ler_btn_tabela_Reserva(self, reserva):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            reserva.lista_btn = []
            with conexao.cursor() as cursor:
                cursor.execute("SELECT nome_btn, nome_tabela, id FROM tabelas_grade_names")
                leitura = cursor.fetchall()

                for linha in leitura:
                    reserva.lista_btn.append(str(linha[0]))
                    reserva.lista_titulo.append(str(linha[1]))
                    reserva.lista_ids.append(str(linha[2]))

        except Exception as e:
            print(f"Error in ler_btn_tabela_Reserva: {e}")
        finally:
            if conexao:
                conexao.close()

    def descobrir_cti(self, grade, id):
        conexao = None
        try:
            conexao = pymysql.connect(**DB_CONFIG)
            grade.lista_btn = []
            with conexao.cursor() as cursor:
                # Corrigindo a sintaxe SQL para verificar se o ID existe
                cursor.execute("SELECT EXISTS(SELECT 1 FROM tabela_ctis WHERE id = %s)", (id,))
                resultado = cursor.fetchone()
                return bool(resultado[0])  # Retorna True se encontrou, False caso contrário

        except Exception as e:
            print(f"Error in descobrir_cti: {e}")
            return False  # Em caso de erro, retorna False
        finally:
            if conexao:
                conexao.close()

    # def definir_posicao_usuario(self, tabela, deman, posicao, tipo):
    #     conexao = None
    #     try:
    #         self.validar_nome_tabela(tabela)
    #
    #         if isinstance(posicao, tuple):
    #             posicao = f"{posicao[0]},{posicao[1]}"
    #
    #         if (tabela != self.tabela_antes or
    #                 posicao != self.posicao_antes or
    #                 tipo != self.tipo_antes):
    #
    #             if tabela != self.tabela_antes:
    #                 posicao = f"{None},{None}"
    #
    #             self.posicao_antes, self.tabela_antes, self.tipo_antes = posicao, tabela, tipo
    #
    #             conexao = pymysql.connect(
    #                 host='10.36.0.32',
    #                 user='sglHC2024',
    #                 password='S4g1L81',
    #                 database='sgl'
    #             )
    #             with conexao.cursor() as cursor:
    #                 cursor.execute(
    #                     '''
    #                     UPDATE posicao_usuario_tempo_real
    #                     SET posicao = %s, tipo = %s, tabela = %s
    #                     WHERE usuario = %s
    #                     ''',
    #                     (posicao, tipo, tabela, deman.user)
    #                 )
    #                 conexao.commit()
    #
    #     except Exception as e:
    #         print(f"Error in definir_posicao_usuario: {e}")
    #     finally:
    #         if conexao:
    #             conexao.close()
    #
    # def ler_posicoes_usuarios(self, tipo, tabela):
    #     conexao = None
    #     try:
    #         self.validar_nome_tabela(tabela)
    #         conexao = pymysql.connect(
    #             host='10.36.0.32',
    #             user='sglHC2024',
    #             password='S4g1L81',
    #             database='sgl'
    #         )
    #         with conexao.cursor() as cursor:
    #             comando = '''
    #                         SELECT usuario, posicao, nome
    #                         FROM posicao_usuario_tempo_real
    #                         WHERE tipo = %s AND tabela = %s
    #                     '''
    #             cursor.execute(comando, (tipo, tabela))
    #             resultados = cursor.fetchall()
    #         return resultados if resultados else False
    #
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return False
    #     finally:
    #         if conexao:
    #             conexao.close()
    #

    # def salvar_historico(self, lista_modificacao, linha_modificada, linha_antiga, colunas):
    #     conexao = None
    #     try:
    #         conexao = pymysql.connect(
    #             host='10.36.0.32',
    #             user='sglHC2024',
    #             password='S4g1L81',
    #             database='sgl'
    #         )
    #         current_datetime = QDateTime.currentDateTime()
    #         formatted_date = current_datetime.toString('dd/MM/yyyy')
    #
    #         linha_antiga_str = json.dumps(linha_antiga, ensure_ascii=False)
    #         linha_modificada_str = json.dumps(linha_modificada, ensure_ascii=False)
    #         colunas_str = json.dumps(colunas, ensure_ascii=False)
    #
    #         with conexao.cursor() as cursor:
    #             for texto in lista_modificacao:
    #                 comando = '''
    #                     INSERT INTO history_demandas
    #                     (data, histo, tabela_no_momento, tabela_alterada, COLUNAS)
    #                     VALUES (%s, %s, %s, %s, %s)
    #                 '''
    #                 valores = (
    #                     formatted_date,
    #                     texto,
    #                     linha_antiga_str,
    #                     linha_modificada_str,
    #                     colunas_str
    #                 )
    #                 cursor.execute(comando, valores)
    #
    #             conexao.commit()
    #
    #     except Exception as e:
    #         print(f"Error saving historico: {e}")
    #     finally:
    #         if conexao:
    #             conexao.close()