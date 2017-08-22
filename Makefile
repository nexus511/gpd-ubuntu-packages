KEY_ID:=F00FA013
MAKE_TARGETS:=$(addsuffix _build,$(shell ls */*/make.py))
REPO_BASE:=repo
REPO_DIR:=$(REPO_BASE)/dists/stable/main/binary
KEYFILE:=common/keyFile

all: $(MAKE_TARGETS)
	make update_repo

%/make.py_build:
	(cd "`dirname "$@"`"; python2 make.py)

update_repo: repo
	cp -v */*/output/*.deb $(REPO_DIR)
	dpkg-sig -k $(KEY_ID) $(REPO_DIR)/*.deb
	cp $(KEYFILE) $(REPO_BASE)
	dpkg-scanpackages -m $(REPO_DIR)        >$(REPO_DIR)/Packages
	cat $(REPO_DIR)/Packages | gzip --fast  >$(REPO_DIR)/Packages.gz
	cat $(REPO_DIR)/Packages | xz -z        >$(REPO_DIR)/Packages.xz
	cat $(REPO_DIR)/Packages | lzma -z      >$(REPO_DIR)/Packages.lz
	rm -f $(REPO_DIR)/InRelease $(REPO_DIR)/Release.gpg
	(cd $(REPO_DIR) ; apt-ftparchive release . > Release ; \
			  gpg --clearsign --digest-algo SHA256 --default-key $(KEY_ID) -o InRelease Release; \
			  gpg --digest-algo SHA256 --default-key $(KEY_ID) -abs -o Release.gpg Release )

repo:
	mkdir -p $(REPO_DIR)
