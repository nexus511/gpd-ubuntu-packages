MAKE_TARGETS=$(addsuffix _build,$(shell ls */*/make.py))

all: $(MAKE_TARGETS)

%/make.py_build:
	(cd "`dirname "$@"`"; python2 make.py)

