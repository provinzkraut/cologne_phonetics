VERSION = $(shell poetry version -s)

.PHONY: test release coverage

coverage:
	python -m coverage erase
	python -m coverage run --source=cologne_phonetics test_cologne_phonetics.py
	python -m coverage report
	python -m coverage html

test:
	python test.py


release: test
	poetry publish
	git add -A
	git tag $(VERSION)
	git push origin HEAD
	git push origin tag $(VERSION)