import subprocess
import random
import re
import datetime

# Nome do arquivo que contém os processos antigos
hoje = datetime.datetime.now().strftime("%d")
arquivo = f"days/{hoje}.txt"

# Função para gerar um número aleatório único
def gerar_numero_randomico():
    return random.randint(10000, 99999)

# Função para verificar se o nome já foi renomeado
def ja_renomeado(nome):
    return bool(re.search(r'\d+$', nome))

# Executa o comando ps e captura a saída
def obter_processos_atuais():
    comando = "ps -eo pid,etime,comm | grep -E '(code|firefox|chrome|terminal)'"
    resultado = subprocess.getoutput(comando).splitlines()
    # Retorna apenas o nome do processo (terceira coluna)
    processos_atuais = [linha.split()[-1] for linha in resultado]
    return processos_atuais

# Função para verificar e renomear processos
def verificar_e_renomear_processos(arquivo, processos_atuais):
    try:
        with open(arquivo, 'r') as f:
            processos_armazenados = [linha.strip() for linha in f.readlines()]
        
        processos_atualizados = []
        
        # Verifica se os processos no arquivo estão nos processos atuais
        for processo in processos_armazenados:
            partes = processo.split()
            if len(partes) >= 3:
                pid = partes[0]
                tempo = partes[1]
                nome = partes[2]
                
                # Se o nome do processo não está na lista de processos atuais e não foi renomeado antes, renomeia
                if nome not in processos_atuais and not ja_renomeado(nome):
                    novo_nome = f"{nome}{gerar_numero_randomico()}"
                    processo_renomeado = f"{pid} {tempo} {novo_nome}"
                    processos_atualizados.append(processo_renomeado)
                else:
                    processos_atualizados.append(processo)
        
        # Atualiza o arquivo com os processos renomeados
        with open(arquivo, 'w') as f:
            for processo in processos_atualizados:
                f.write(processo + '\n')
        
        print(f"Arquivo {arquivo} atualizado com sucesso.")

    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executa o script
processos_atuais = obter_processos_atuais()
verificar_e_renomear_processos(arquivo, processos_atuais)

