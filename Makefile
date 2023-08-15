
PY=py
VERS=0.0.1a0
INSTALLED := $(shell $(PY) -c "import importlib.util; target = importlib.util.find_spec('dsapy'); print(target is not None)")

all: build install test

test:
	shell mypy .\src\dsapy
	@echo "testing..."
ifeq ($(INSTALLED),True)
	@echo "testing..."
endif

build:
	$(PY) -m pip install -q build
	$(PY) -m build

install:
ifeq ($(INSTALLED),True)
	$(PY) -m pip uninstall dsapy
endif
	$(PY) -m pip install dist/dsapy-$(VERS).tar.gz

clean:
	- del /S .\dist\*
