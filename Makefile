# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)
S3BUCKET = s.hdimg.net

default: dependencies test
# CMD=sudo
CMD=

dependencies:
	virtualenv pythonenv
	pip install -E pythonenv -r requirements.txt

.PHONY: coverage test build clean install upload check deploy
