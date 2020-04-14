all:
	rm -f dist/*
	/usr/bin/python3.6 setup.py sdist bdist_wheel
	sed -i 's+#!python+#!/usr/bin/python3+g' build/scripts-3.6/bpview
	sed -i 's+#!python+#!/usr/bin/python3+g' build/scripts-3.6/bpmerge

testdist:
	python3.6 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

testinstall:
	python3.6 -m pip install --index-url https://test.pypi.org/simple --no-deps plxr

