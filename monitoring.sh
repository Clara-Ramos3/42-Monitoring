#!/bin/bash

HOJE=$(date '+%d')
OUTPUT_FILE="$HOJE.txt"
TEMP_FILE="temp_processos.txt"

# Executa o comando e redireciona a saída para o arquivo 'processos.txt'
 ps -eo pid,etime,comm | grep -E "(code|firefox|chrome|terminal)" > $TEMP_FILE

# se o arquivo do dia já existe
if ([ -f $OUTPUT_FILE ]); then
	# Combina novas entradas com as existentes, ordena e remove duplicadas
	cat $TEMP_FILE | sort | uniq > combined.txt
	cat $OUTPUT_FILE | sort | uniq >> combined.txt
	sort combined.txt | uniq > $OUTPUT_FILE
	rm combined.txt
else
	# Se o arquivo nao existe, renomeie o arquivo temporario
	mv $TEMP_FILE $OUTPUT_FILE
fi

# removendo o arquivo tempporario
if [[ -f $TEMP_FILE ]]; then
	rm $TEMP_FILE
fi

# Mensagem de sucesso
echo "Os processos foram listados no arquivo dia.txt"

