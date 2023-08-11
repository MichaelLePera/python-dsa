
PY=py -m
VERS=0.0.1a0

all: build

build:
	$(PY) pip install -q build
	$(PY) build
	$(PY) pip install dist/dsapy-$(VERS).tar.gz

clean:
	rm -rf ./dist/*
