import sqlite3
import os
import datetime
import time

# Caminho para o banco de dados do histórico do Opera
opera_db_path = os.path.expanduser("~/.config/opera/History")  # Ajuste se necessário
# Nome do arquivo que irá armazenar o histórico filtrado
arquivo_saida = "history/opera.txt"

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

# Função para acessar o histórico do Firefox
def acessar_historico_firefox():
    max_attempts = 5
    attempt = 0
    historico_novo = []

    while attempt < max_attempts:
        try:
            # Caminho para o banco de dados do Firefox
            firefox_profile = os.path.expanduser("~/.mozilla/firefox/")
            for folder in os.listdir(firefox_profile):
                if folder.endswith(".default-release"):
                    firefox_db_path = os.path.join(firefox_profile, folder, "places.sqlite")
                    break
            
            conn = sqlite3.connect(firefox_db_path)
            cursor = conn.cursor()

            # Carrega o histórico existente para evitar duplicações
            historico_existente = carregar_historico_existente()

            # Consulta para obter URLs acessadas hoje
            consulta = f"""
                SELECT url, title, datetime(last_visit_date/1000000, 'unixepoch') as visit_time
                FROM moz_places
                WHERE last_visit_date >= strftime('%s', 'now', 'localtime', 'start of day') * 1000000
                ORDER BY last_visit_date DESC
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
            print("O banco de dados do Firefox está bloqueado. Tentando novamente...")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
            attempt += 1

    return historico_novo

# Função para acessar o histórico do Opera
def acessar_historico_opera():
    max_attempts = 5
    attempt = 0
    historico_novo = []

    while attempt < max_attempts:
        try:
            conn = sqlite3.connect(opera_db_path)
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
            print("O banco de dados do Opera está bloqueado. Tentando novamente...")
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
            attempt += 1

    return historico_novo

# Coleta o histórico do navegador Firefox
historico_firefox = acessar_historico_firefox()
# Coleta o histórico do navegador Opera
historico_opera = acessar_historico_opera()

# Salva o histórico coletado em um arquivo
salvar_novo_historico(historico_firefox + historico_opera)

print("Histórico de hoje salvo com sucesso.")

