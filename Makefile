clean:
	rm -rf build
	rm -rf dist

build:
	python build.py

publish:
	python release.py

.PHONY: clean build publish
