HYPOTHESIS_PROFILE=slow

SOURCES=twelvefactor.py tests.py examples/example.py

test:
	py.test 

release:
	python scripts/release.py

format:
	isort -rc $(SOURCES)
	pyformat --in-place $(SOURCES)

lint:
	flake8 $(SOURCES) --exclude=_compat.py

ci: lint
	tox -- --hypothesis-profile=$(HYPOTHESIS_PROFILE)

docs:
	$(MAKE) -C docs html

.PHONY: test release format lint ci docs