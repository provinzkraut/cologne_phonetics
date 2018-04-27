VERSION = $(shell python3 setup.py --version)

.PHONY: test test_all test_34 test_35 test_36 release

test_all: test_34 test_35 test_36

test:
	python3 test_cologne_phonetics.py

test_34:
	python3.4 test_cologne_phonetics.py

test_35:
	python3.5 test_cologne_phonetics.py

test_36:
	python3.6 test_cologne_phonetics.py

release: test_all
	python3 setup.py sdist bdist_wheel
	git add -A
	git tag $(VERSION)
	git push origin HEAD
	git push origin tag $(VERSION)
	twine upload dist/*
