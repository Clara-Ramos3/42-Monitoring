16 Outubro 2024

 - comando 1: listar tudo usado na conta enquanto logado
	ps -eo pid,etime,comm | grep -E "(code|firefox|chrome)"

 - comando 2: deletar uma linha espeifica de um arquivo .txt
	sed -i '/string_a_procurar/d' nome_do_arquivo.txt

 - comando 3: rodar o arquivo python que filtra os semelhantes e busca o de maior valor
 	python3 filter.py
 - comando 4: ajustando os dados buscados, em caso de abrir e fechar muitos processos
 	python3 ajust.py
 - comando 5: coletar os users 
 	echo "$USER"
 - comando 6: fazer o script rodar de maneira autonoma de tempo em tempo
	crontab -e
	#Adicionado o caminho para o script dentro do crontab
	@reboot /caminho/completo/para/o/script/hello_loop.sh
 - comando 7: rodar o script sempre que existir inicio de sessao
 	#raquear sistema criando um bash_profile
	cat ~/.bash_profile
 - comando 8: enviando arquivos ou informacoes para o pythonanywhere
	curl -X POST -F "username=$user" -F "message=$message" https://teu_user.pythonanywhere.com/register

