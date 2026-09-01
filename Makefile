PYTHON ?= python3
APP = calculator:app
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: help install run dev test lint clean

help:
	@echo "Available targets:"
	@echo "  make install   Install project dependencies"
	@echo "  make run       Start the FastAPI app"
	@echo "  make dev       Start app in reload mode"
	@echo "  make test      Run a quick API smoke test"
	@echo "  make lint      Run basic Python syntax validation"
	@echo "  make clean     Remove Python cache files"

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m uvicorn $(APP) --host $(HOST) --port $(PORT)

dev:
	$(PYTHON) -m uvicorn $(APP) --host $(HOST) --port $(PORT) --reload

test:
	$(PYTHON) -c "from fastapi.testclient import TestClient; from calculator import app; client = TestClient(app); response = client.post('/api/calc', json={'expression': '2+3*4'}); assert response.status_code == 200, response.text; assert response.json()['result'] == 14; print('API smoke test passed')"

lint:
	$(PYTHON) -m compileall calculator.py

clean:
	find . -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.mypy_cache' \) -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
