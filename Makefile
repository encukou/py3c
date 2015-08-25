all:
	echo "Available targets:"
	echo "    make test"
	echo "    make test-<interpreter>"

test:
	$(MAKE) test-python2
	$(MAKE) test-python3

# TODO: A better way to build & use one-off extensions?

build-%:
	cd test; rm -rvf build ; $* setup.py build

test-%: build-%
	PYTHONPATH=$(wildcard test/build/lib*) $* test -v

.PHONY: test
