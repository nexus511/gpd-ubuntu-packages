KEY_ID:=F00FA013
MAKE_TARGETS:=$(addsuffix _build,$(shell ls */*/make.py))
REPO_BASE:=repo
REPO_DIR:=$(REPO_BASE)/dists/stable/main/binary
KEYFILE:=common/keyFile

all: $(MAKE_TARGETS)
	make update_repo

%/make.py_build:
	(cd "`dirname "$@"`"; python2 make.py)

update_kernel: external/kernel
	(cd $< ; make -j9 INSTALL_MOD_PATH=`realpath ./MODULES` all modules modules_install )
	tar -cjf bootstrap-kernel-lib.tar.bz2 -C external/kernel/MODULES/ .
	mkdir -p build/boot
	cp external/kernel/System.map build/boot/System.map-`cat external/kernel/include/config/kernel.release`
	cp external/kernel/.config build/boot/config-`cat external/kernel/include/config/kernel.release`
	cp external/kernel/arch/x86_64/boot/bzImage build/boot/vmlinuz-`cat external/kernel/include/config/kernel.release`
	tar -cjf bootstrap-kernel-boot.tar.bz2 -C build/ .
	rm -rf build
	mv bootstrap-kernel-lib.tar.bz2 bootstrap-kernel-boot.tar.bz2 packages/linux-image-gpdpocket/files/

update_repo: repo
	cp -v */*/output/*.deb $(REPO_DIR)
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

images: update_repo
	(cd respin && make)

repo:
	mkdir -p $(REPO_DIR)
