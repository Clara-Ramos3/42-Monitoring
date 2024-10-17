import datetime  # Adicione esta linha para importar a biblioteca datetime

# Nome do arquivo que contém os processos
hoje = datetime.datetime.now().strftime("%d")  # Apenas o dia do mês
arquivo = f"days/{hoje}.txt"

# Dicionário para armazenar os maiores processos
maior_processos = {}

# Função para converter tempo em segundos
def tempo_para_segundos(tempo):
    partes = list(map(int, tempo.split(':')))
    if len(partes) == 3:  # HH:MM:SS
        return partes[0] * 3600 + partes[1] * 60 + partes[2]
    else:  # MM:SS
        return partes[0] * 60 + partes[1]

# Lê o arquivo e processa cada linha
try:
    with open(arquivo, 'r') as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) < 3:
                continue

            pid = partes[0]
            tempo = partes[1]
            nome = partes[2]

            total_segundos = tempo_para_segundos(tempo)

            # Atualiza o maior processo para cada nome
            if nome not in maior_processos or total_segundos > maior_processos[nome][1]:
                maior_processos[nome] = (linha.strip(), total_segundos)

    # Escreve os resultados de volta no arquivo
    with open(arquivo, 'w') as f:
        for processo in maior_processos.values():
            f.write(processo[0] + '\n')

    print("Linhas duplicadas removidas. Somente a linha com o maior tempo para cada processo foi mantida.")

except FileNotFoundError:
    print(f"O arquivo {arquivo} não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

