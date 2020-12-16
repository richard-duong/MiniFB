
network:
	sudo mn --custom src/finalTopol.py --topo finaltopol -x

client:
	python -B src/client.py 10.0.0.4

server:
	python -B src/server.py
