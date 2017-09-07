package=reprep
include pypackage.mk
	
demos:
	rm -rf reprep_demos_out
	reprep_demos


bump-upload:
	bumpversion patch
	git push --tags
	git push --all
	rm -f dist/*
	python setup.py sdist
	twine upload dist/*
	