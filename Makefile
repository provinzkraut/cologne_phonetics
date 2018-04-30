VERSION = $(shell python3 setup.py --version)

.PHONY: test test_all test_34 test_35 test_36 test_37 test_pypy release coverage

coverage:
	python3 -m coverage erase
	python3 -m coverage run --source=cologne_phonetics test_cologne_phonetics.py
	python3 -m coverage report
	python3 -m coverage html

test_all: test_34 test_35 test_36 test_37 test_pypy

test:
	python3 test_cologne_phonetics.py

test_pypy:
	pypy3 test_cologne_phonetics.py

test_34:
	python3.4 test_cologne_phonetics.py

test_35:
	python3.5 test_cologne_phonetics.py

test_36:
	python3.6 test_cologne_phonetics.py

test_37:
	python3.7 test_cologne_phonetics.py

release: test_all
	python3 setup.py sdist bdist_wheel
	git add -A
	git tag $(VERSION)
	git push origin HEAD
	git push origin tag $(VERSION)
	twine upload dist/*
