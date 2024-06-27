.PHONY: ins
ins:
		poetry install
		.\.venv\Scripts\activate
		poetry add fastapi
		poetry add flake8
		poetry add black
		poetry add isort
		poetry add pytest
