16 Outubro 2024

 - comando 1: listar tudo usado na conta enquanto logado
	ps -eo pid,etime,comm | grep -E "(code|firefox|chrome)"
