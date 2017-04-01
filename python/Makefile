.PHONY: test upload

test:
	pytest tests/

upload: test
	python setup.py sdist bdist_wheel upload
