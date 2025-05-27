.PHONY: install run test lint format

install:
	uv venv
	source .venv/bin/activate && uv pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	PYTHONPATH=. pytest -v

lint:
	ruff check .

format:
	ruff format .
