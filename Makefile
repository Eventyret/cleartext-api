.PHONY: run test lint format

run:
	uvicorn app.main:app --reload

test:
	PYTHONPATH=. pytest -v

lint:
	ruff check .

format:
	ruff format .
