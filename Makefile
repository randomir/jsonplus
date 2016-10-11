.PHONY: build upload

build:
	python setup.py sdist
	python setup.py bdist_wheel

upload:
	python setup.py sdist upload
