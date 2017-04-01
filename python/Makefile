.PHONY: test upload

test:
	py.test tests/

upload: test
	python setup.py sdist bdist_wheel upload
