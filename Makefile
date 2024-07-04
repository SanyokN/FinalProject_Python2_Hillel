.PHONY: ins
ins:
		pip install poetry
		poetry config --local virtualenvs.in-project true
		poetry init -n
		poetry install
		.\.venv\Scripts\activate
		poetry add fastapi
		poetry add flake8
		poetry add black
		poetry add isort
		poetry add pytest

.PHONY: c
c:
	@echo 'Starting code correction...'
	black .
	isort .
	flake8 .
	pytest .
	@echo 'FINISH'
