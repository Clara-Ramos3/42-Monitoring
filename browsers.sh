#!/bin/bash

# Função para verificar se o processo está ativo e executar o script correspondente
verifica_e_executa() {
    local processo="$1"
    local script="$2"
    
    if ! pgrep "$processo" > /dev/null; then
        echo "O processo '$processo' não está ativo. Executando $script..."
        cd navegadores && python3 "$script"
        cd ..
    else
        echo "'$processo' está ativo."
    fi
}

# Verifica cada processo
verifica_e_executa "chromium" "chromium.py"
verifica_e_executa "firefox" "firefox.py"
verifica_e_executa "chrome" "chrome.py"
verifica_e_executa "brave" "brave.py"
verifica_e_executa "opera" "opera.py"

