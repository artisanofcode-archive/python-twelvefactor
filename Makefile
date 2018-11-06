HYPOTHESIS_PROFILE ?= fast

SOURCES=$(shell find . -name '*.py')

test:
	poetry run python -m pytest --hypothesis-profile=$(HYPOTHESIS_PROFILE) --cov . --cov-report html --cov-report term-missing tests

fmt:
	poetry run isort -m 3 -tc -fgw 0 -ca -w 79 $(SOURCES)
	poetry run docformatter --blank --make-summary-multi-line --pre-summary-newline -i $(SOURCES)
	poetry run black $(SOURCES)

lint:
	poetry run isort -m 3 -tc -fgw 0 -ca -w 79 -c $(SOURCES)
	poetry run black --check $(SOURCES)
	poetry run flake8 --max-complexity 5 $(SOURCES)
	poetry run bandit ./twelvefactor.py
	poetry run mypy --ignore-missing-imports --strict $(SOURCES) 

ci: test lint docs

docs:
	poetry run $(MAKE) -C docs html

.PHONY: test release format lint ci docs
