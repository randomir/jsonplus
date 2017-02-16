.PHONY: test upload

test:
	cd tests/ && pytest

upload: test
	python setup.py sdist bdist_wheel upload
