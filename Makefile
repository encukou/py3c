all:
	echo "Available targets:"
	echo "    make test"

test:
	$(MAKE) test-python2
	$(MAKE) test-python3

# TODO: A better way to build & use one-off extensions?

nuild-%:
	cd test; rm -rvf build ; $* setup.py build

test-%: nuild-%
	PYTHONPATH=$(wildcard test/build/lib*) $* test -v

.PHONY: test
