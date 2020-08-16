clean:
	rm -rf build
	rm -rf dist

build:
	python convert.py

publish:
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [[ "$BRANCH" != "release" ]]; then
        echo 'Aborting script';
        exit 1;
    fi
    version=$(head -n 1 VERSION)
	githubrelease release Jerakin/p5e-foundryVTT create 'v$version' --publish --name 'v$version' "dist/Pokemon5e.zip"

.PHONY: clean build publish
