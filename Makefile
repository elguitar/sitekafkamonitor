installdeps:
	pip3 install -r requirements.txt

startmonitor:
	python3 sitemonitor/main.py

startwriter:
	python3 databasewriter/main.py

test:
	pytest

