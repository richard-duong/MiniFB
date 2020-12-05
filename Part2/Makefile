PY='python'
PYFLAGS='-B'
HOST='10.0.2.15'
PORT='9999'

all: server.py client.py	

server.py:
	$(PY) $(PYFLAGS) server.py $(PORT)

client.py:
	$(PY) $(PYFLAGS) client.py $(HOST) $(PORT)


