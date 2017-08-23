IMAGE_SOURCE:=
IMAGE_NAME:=$(notdir $(IMAGE_SOURCE))
IMAGE_FILE:=images/$(IMAGE_NAME)
IMAGE_TMP:=tmp/$(IMAGE_NAME)

TMP_MOUNT:=$(IMAGE_TMP)/mnt
MOUNT_ISO:=$(TMP_MOUNT)/iso
MOUNT_SQUASH:=$(TMP_MOUNT)/squashfs

TMP_CLONE:=$(IMAGE_TMP)/data
CLONE_ISO:=$(TMP_CLONE)/iso
CLONE_SQUASH:=$(TMP_CLONE)/squashfs

IMAGE_SQUASH:=$(CLONE_ISO)/casper/filesystem.squashfs

ROOT:=$(CLONE_SQUASH)
REPO_BASE:=../repo
REPO:=$(REPO_BASE)/dists/stable/main/binary
KEYFILE:=$(REPO_BASE)/keyFile

define mount_pseudofs
  if [ ! -f "$(IMAGE_TMP)/.mounted" ]; then \
		mount --bind /proc $(ROOT)/proc; \
		mount --bind /dev $(ROOT)/dev; \
		mount --bind /sys $(ROOT)/sys; \
		mount --bind /dev/pts $(ROOT)/dev/pts; \
		mv $(ROOT)/etc/resolv.conf $(ROOT)/etc/resolv.conf.distrib; \
		cp /etc/resolv.conf $(ROOT)/etc/resolv.conf; \
		touch $(IMAGE_TMP)/.mounted; \
	fi
endef

define umount_pseudofs
	if [ -f "$(IMAGE_TMP)/.mounted" ]; then \
	  mv $(ROOT)/etc/resolv.conf.distrib $(ROOT)/etc/resolv.conf ;\
		umount $(ROOT)/dev/pts; \
		umount $(ROOT)/proc; \
		umount $(ROOT)/dev; \
		umount $(ROOT)/sys; \
		rm $(IMAGE_TMP)/.mounted; \
	fi
endef

respin: install_packages

fetch_image: $(IMAGE_FILE)

$(IMAGE_FILE):
	wget "$(IMAGE_SOURCE)" -O "$@"
	grep -F "$@" files/iso.hashes.sha256sum  | sha256sum --check -

$(IMAGE_TMP)_clean: .PHONY
	rm -rf $(IMAGE_TMP)

$(CLONE_ISO): $(IMAGE_FILE) $(IMAGE_TMP)_clean
	mkdir -p $(MOUNT_ISO) $@
	mount -o loop $< $(MOUNT_ISO)
	rsync -a $(MOUNT_ISO)/. $@
	umount $<

$(IMAGE_SQUASH): $(CLONE_ISO)

$(CLONE_SQUASH): $(IMAGE_SQUASH)
	mkdir -p $(MOUNT_SQUASH) $@
	mount -o loop $< $(MOUNT_SQUASH)
	rsync -a $(MOUNT_SQUASH)/. $@
	umount $<

$(IMAGE_TMP)/MOUNTED: $(ROOT)

install_packages: $(CLONE_SQUASH)
	$(call mount_pseudofs)
	mv $(ROOT)/etc/resolv.conf $(ROOT)/etc/resolv.conf.distrib
	cp /etc/resolv.conf $(ROOT)/etc/resolv.conf

	echo "copy our local repository to target"
	rsync -va $(REPO)/. $(ROOT)/tmp/repo
	cp -v $(KEYFILE) $(ROOT)/tmp/keyfile

	echo "install our keys on the target"
	chroot $(ROOT) apt-key add /tmp/keyfile

	echo "install packages from local repo"
	cp $(ROOT)/etc/apt/sources.list $(ROOT)/etc/apt/sources.list.distrib
	echo "deb file:///tmp/repo /" >> $(ROOT)/etc/apt/sources.list
	echo "deb http://de.archive.ubuntu.com/ubuntu/ xenial universe" >> $(ROOT)/etc/apt/sources.list
	chroot $(ROOT) apt -y install gpdpocket gpdpocket-xfce-config

	echo "rollback changes on apt configuration and add our repository"
	mv $(ROOT)/etc/apt/sources.list.distrib $(ROOT)/etc/apt/sources.list

	#echo "perform full system upgrade as we have actually updated the sources"
	#chroot $(ROOT) apt update
	#chroot $(ROOT) apt -y upgrade

	echo "add our repository to ensure that future updates are possible"
	echo "deb https://apt.nexus511.net/repo/dists/stable/main/binary /" >>$(ROOT)/etc/apt/sources.list
	chroot $(ROOT) apt update

	echo "cleanup old files"
	rm -rf $(ROOT)/tmp/repo $(ROOT)/tmp/keyfile
	$(call umount_pseudofs)

.PHONY:
