KEY_ID:=F00FA013
MAKE_TARGETS:=$(addsuffix _build,$(shell ls */*/make.py))
REPO_BASE:=repo
REPO_DIR:=$(REPO_BASE)/dists/stable/main/binary
KEYFILE:=common/keyFile

all:

packages: $(MAKE_TARGETS)
	make update_repo


%/make.py_build:
	(cd "`dirname "$@"`"; python2 make.py)

external/kernel/.kernel_patched: external/kernel
	(cd external/kernel && bash ./patch_kernel )

build_kernel: external/kernel/.kernel_patched
	rm -rf external/*.deb packages/prebuilt
	(cd external/kernel && bash ./build_kernel )
	mkdir -p packages/prebuilt/output
	mv external/*.deb packages/prebuilt/output

update_repo: repo
	cp -v packages/*/output/*.deb $(REPO_DIR)
	(cd $(REPO_DIR); dpkg-sig -k $(KEY_ID) *.deb)
	cp $(KEYFILE) $(REPO_BASE)
	(cd $(REPO_DIR); dpkg-scanpackages -m . >Packages)
	cat $(REPO_DIR)/Packages | gzip --fast  >$(REPO_DIR)/Packages.gz
	cat $(REPO_DIR)/Packages | xz -z        >$(REPO_DIR)/Packages.xz
	cat $(REPO_DIR)/Packages | lzma -z      >$(REPO_DIR)/Packages.lz
	rm -f $(REPO_DIR)/InRelease $(REPO_DIR)/Release.gpg
	(cd $(REPO_DIR) ; apt-ftparchive release . > Release ; \
			  gpg --clearsign --digest-algo SHA256 --default-key $(KEY_ID) -o InRelease Release; \
			  gpg --digest-algo SHA256 --default-key $(KEY_ID) -abs -o Release.gpg Release )

sync_repo: update_repo
	rsync -va --delete repo/. ssh-rsa nexus511.repo:htdocs/repo_testing

images: update_repo
	(cd respin && make)

repo:
	mkdir -p $(REPO_DIR)

