all:
	python3 main.py

class:
	python3 classes.py

client:
	python3 client.py

scene:
	python3 scene.py

api:
	open http://127.0.0.1:8000 ; \
	python3 -m uvicorn main:app --reload
