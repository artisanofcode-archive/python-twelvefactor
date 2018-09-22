HYPOTHESIS_PROFILE=fast

SOURCES=twelvefactor.py tests.py examples/example.py

test:
	poetry run python -m pytest --hypothesis-profile=$(HYPOTHESIS_PROFILE) tests.py

fmt:
	poetry run isort -rc $(SOURCES)
	poetry run pyformat --in-place $(SOURCES)

lint:
	poetry run flake8 $(SOURCES)

ci: test lint docs

docs:
	poetry run $(MAKE) -C docs html

.PHONY: test release format lint ci docs