import sqlite3
import os
import datetime
import time

# Caminho para o banco de dados do histórico do Brave
brave_db_path = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/History")  # Ajuste se necessário
# Nome do arquivo que irá armazenar o histórico filtrado
arquivo_saida = "history/brave.txt"

# Obtém a data de hoje
hoje = datetime.datetime.now().strftime("%Y-%m-%d")

# Função para carregar histórico anterior, caso o arquivo exista
def carregar_historico_existente():
    historico_existente = set()
    if os.path.exists(arquivo_saida):
        with open(arquivo_saida, 'r') as file:
            for linha in file:
                historico_existente.add(linha.strip())
    return historico_existente

# Função para salvar o histórico atualizado
def salvar_novo_historico(historico_novo):
    with open(arquivo_saida, 'a') as file:
        for linha in historico_novo:
            file.write(linha + '\n')

# Função para acessar o histórico do Brave
def acessar_historico_brave():
    max_attempts = 5
    attempt = 0
    historico_novo = []

    while attempt < max_attempts:
        try:
            conn = sqlite3.connect(brave_db_path)
            cursor = conn.cursor()

            # Carrega o histórico existente para evitar duplicações
            historico_existente = carregar_historico_existente()

            # Consulta para obter URLs acessadas hoje
            consulta = f"""
                SELECT url, title, datetime(last_visit_time/1000000, 'unixepoch') as visit_time
                FROM urls
                WHERE last_visit_time >= strftime('%s', 'now', 'localtime', 'start of day') * 1000000
                ORDER BY last_visit_time DESC
            """

            # Executa a consulta
            cursor.execute(consulta)

            # Verifica se o histórico já existe no arquivo e adiciona apenas os novos
            for row in cursor.fetchall():
                url = row[0]
                title = row[1]
                visit_time = row[2]
                linha = f"URL: {url}\nTitle: {title}\nLast Visit: {visit_time}\n"
                
                if linha not in historico_existente:
                    historico_novo.append(linha)

            # Fecha a conexão com o banco de dados
            conn.close()
            break  # Saia do loop se tudo correr bem

        except sqlite3.OperationalError:
            print("O banco de dados do Brave está bloqueado. Tentando novamente...")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
            attempt += 1

    return historico_novo

# Coleta o histórico do navegador Brave
historico_brave = acessar_historico_brave()

# Salva o histórico coletado em um arquivo
salvar_novo_historico(historico_brave)

print("Histórico de hoje salvo com sucesso.")

