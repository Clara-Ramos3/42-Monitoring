#!/bin/bash

# Função para verificar o status da execução
verificar_status() {
    if [ $? -ne 0 ]; then
        echo "Ocorreu um erro ao executar $1. Abortando execução."
        exit 1
    fi
}

echo "Executando script shell monitoring"
./monitoring.sh
verificar_status "monitoring.sh"

echo "Executando script Python filter"
python3 filter.py
verificar_status "filter.py"

echo "Executando script Python ajust"
python3 ajust.py
verificar_status "ajust.py"

echo "Todos os scripts foram executados com sucesso!"

clear
echo "All Done!"

