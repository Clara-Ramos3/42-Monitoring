16 Outubro 2024

 - comando 1: listar tudo usado na conta enquanto logado
	ps -eo pid,etime,comm | grep -E "(code|firefox|chrome)"

 - comando 2: deletar uma linha espeifica de um arquivo .txt
	sed -i '/string_a_procurar/d' nome_do_arquivo.txt
