# Antes de instalar, chequear en rotulator.py que el sheabang sea el adecuado. En algunos sistemas se llama python3 y en otros solo python

rotulator: rotulator.py
	cp rotulator.py rotulator
	chmod +x rotulator

install: rotulator
	mv rotulator /usr/local/bin

uninstall:
	rm /usr/local/bin/rotulator

.PHONY: install uninstall
