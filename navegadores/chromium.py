import sqlite3
import os
import datetime
import time

# Caminho para o banco de dados do histórico do Chromium
chromium_db_path = os.path.expanduser("~/.config/chromium/Default/History")
# Nome do arquivo que irá armazenar o histórico filtrado
arquivo_saida = "historico_de_hoje.txt"

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

# Tentativa de conexão ao banco de dados do histórico do Chromium com retry
max_attempts = 5
attempt = 0
while attempt < max_attempts:
    try:
        conn = sqlite3.connect(chromium_db_path)
        cursor = conn.cursor()
        
        # Carrega o histórico existente para evitar duplicações
        historico_existente = carregar_historico_existente()

        # Consulta para obter URLs acessadas hoje, incluindo o título
        consulta = f"""
            SELECT url, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch') as visit_time
            FROM urls
            WHERE visit_time LIKE '{hoje}%'
            ORDER BY visit_time DESC
        """

        # Executa a consulta
        cursor.execute(consulta)

        # Armazena os novos registros que serão adicionados
        historico_novo = []

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

        # Se houver novos registros, salva no arquivo
        if historico_novo:
            salvar_novo_historico(historico_novo)
            print("Novos registros adicionados ao histórico de hoje.")
        else:
            print("Nenhum novo registro encontrado.")
        
        break  # Saia do loop se tudo correr bem

    except sqlite3.OperationalError:
        print("O banco de dados está bloqueado. Tentando novamente...")
        time.sleep(1)  # Espera 1 segundo antes de tentar novamente
        attempt += 1

if attempt == max_attempts:
    print("Não foi possível acessar o banco de dados após várias tentativas.")

