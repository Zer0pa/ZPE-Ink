PYTHON ?= python3

.PHONY: install install-dev test build demo smoke contract bindings

install:
	$(PYTHON) -m pip install -e ./code

install-dev:
	$(PYTHON) -m pip install -e './code[dev]'

test:
	$(PYTHON) -m pytest code/tests -q

build:
	$(PYTHON) -m build --wheel --sdist ./code --outdir dist

demo:
	$(PYTHON) -m zpe_ink demo

smoke:
	$(PYTHON) -m zpe_ink verify-roundtrip

contract:
	$(PYTHON) code/scripts/verify_binding_contracts.py --repo-root .

bindings:
	PYO3_PYTHON="$(PYTHON)" cargo check --manifest-path code/bindings/python_native/Cargo.toml
	cargo check --manifest-path code/bindings/wasm/Cargo.toml --target wasm32-unknown-unknown
