#!/bin/bash

HOJE=$(date '+%d')

# Executa o comando e redireciona a saída para o arquivo 'processos.txt'
ps -eo pid,etime,comm | grep -E "(code|firefox|chrome)" > $HOJE.txt

# Mensagem de sucesso
echo "Os processos foram listados no arquivo dia.txt"

