.PHONY: demo upload

demo:
	# TODO: use ``envie`` to build venv if it doesn't exist
	cd test/ && . env/bin/activate && FLASK_APP=demo.py FLASK_DEBUG=1 flask run

upload:
	python setup.py sdist bdist_wheel upload
