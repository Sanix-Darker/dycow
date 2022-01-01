isort = ./env/bin/python3 -m isort dycow tests
black = ./env/bin/python3 -m black dycow tests
flake8 = ./env/bin/python3 -m flake8 dycow tests

set-env:
	virtualenv -p python3 env

install:
	./env/bin/pip install -r build-requirements.txt

build: install
	echo "We remove unecessary files/folders"
	echo "----------------------------------"
	rm -rf build/*
	rm -rf dist/*
	rm -rf *-info
	echo "----------------------------------\n"
	echo "python3 setup.py sdist bdist_wheel"
	./env/bin/python3 setup.py sdist bdist_wheel

publish: build
	echo "python3 -m twine upload dist/*"
	./env/bin/python3 -m twine upload dist/*
	echo "----------------------------------\n"
	echo "We remove unecessary files/folders"
	rm -rf build/*
	rm -rf dist/*
	rm -rf *-info
	echo "----------------------------------\n"

format:
	$(isort)
	$(black)

lint:
	$(flake8)
	$(isort) --check-only --df
	$(black) --check --diff
