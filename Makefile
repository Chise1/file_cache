checkfiles = file_cache/ tests/ conftest.py
black_opts = -l 80 -t py38
py_warn = PYTHONDEVMODE=1
test_settings = SETTINGS_MODULE=tests.settings

help:
	@echo "file_cache development makefile"
	@echo
	@echo  "usage: make <target>"
	@echo  "Targets:"
	@echo  "    up			Updates dev/test dependencies"
	@echo  "    deps		Ensure dev/test dependencies are installed"
	@echo  "    check		Checks that build is sane"
	@echo  "    test		Runs all tests"
	@echo  "    style		Auto-formats the code"

up:
	@poetry update

deps:
	@poetry install --no-root

style: deps
	isort -src $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	flake8 $(checkfiles)
	bandit -x test -r $(checkfiles)

test: deps
	$(py_warn) $(test_settings) py.test