PYLINT_DISABLE := maybe-no-member,missing-docstring

.PHONY: all
all: clean test build lint

.PHONY: venv
venv:
	virtualenv venv -p python3
	/usr/bin/env bash -c "source venv/bin/activate && \
		pip install -r requirements.txt"

.PHONY: lint
lint: venv
	/usr/bin/env bash -c "source venv/bin/activate && pylint dataflowlauncher test --disable=$(PYLINT_DISABLE)"

.PHONY: test
test: venv
	/usr/bin/env bash -c "source venv/bin/activate && python3 -m unittest"

.PHONY: build
build: test
	/usr/bin/env bash -c "source venv/bin/activate && \
		pex --disable-cache . -v -e dataflowlauncher.launcher -o target/dataflow_launcher.pex --python=python3 "

.PHONY: clean
clean:
	find . -name *.pyc | xargs rm -rf
	find . -name __pycache__ | xargs rm -rf
	rm -rf target
	rm -rf build
	rm -rf venv
