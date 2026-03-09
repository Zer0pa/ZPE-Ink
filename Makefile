PYTHON ?= python3

.PHONY: install test build demo smoke

install:
	$(PYTHON) -m pip install -e ./code

test:
	$(PYTHON) -m pytest code/tests -q

build:
	$(PYTHON) -m pip wheel ./code --no-deps -w dist

demo:
	PYTHONPATH=code $(PYTHON) executable/demo.py

smoke:
	PYTHONPATH=code $(PYTHON) executable/verify_roundtrip.py
