package=reprep
include pypackage.mk

demos:
	rm -rf reprep_demos_out
	reprep_demos


bump:
	bumpversion --verbose patch

upload:
	git push --tags
	git push --all
	rm -f dist/*
	rm -rf src/*.egg-info
	python setup.py sdist
	twine upload --verbose dist/*

bump-upload:
	$(MAKE) bump
	$(MAKE) upload

name=reprep-python3

test-python3:
	docker stop $(name) || true
	docker rm $(name) || true

	docker run -it -v "$(shell realpath $(PWD)):/reprep" -w /reprep --name $(name) python:3 /bin/bash

test-python3-install:
	pip install -r requirements.txt
	pip install nose
	python setup.py develop --no-deps

