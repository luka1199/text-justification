PYTHON = python
CHECKSTYLE = flake8
TEST_BINARIES = $(wildcard *Test.py)

all: compile test checkstyle

compile:
	@echo "Nothing to compile for Python :-)"

test: $(TEST_BINARIES)
	for T in $(TEST_BINARIES); do $(PYTHON) $$T; done

checkstyle:
	$(CHECKSTYLE) *.py

clean:
	rm -f *.pyc
