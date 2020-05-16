.DEFAULT_GOAL := help

.PHONY: format
format:  ## Auto-format and check pep8
	pipenv run yapf -i $$(find * -type f -name '*.py')
	pipenv run flake8 .