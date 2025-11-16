install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run # имитация процесса загрузки в PyPI

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run ruff cpoetry env activateheck .