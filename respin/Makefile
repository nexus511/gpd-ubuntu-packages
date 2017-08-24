UBUNTU_16_04_3:=http://releases.ubuntu.com/16.04/ubuntu-16.04.3-desktop-amd64.iso
UBUNTU_17_04:=http://releases.ubuntu.com/17.04/ubuntu-17.04-desktop-amd64.iso
XUBUNTU_16_04_1:=http://cdimage.ubuntu.com/xubuntu/releases/16.04/release/xubuntu-16.04.1-desktop-amd64.iso
XUBUNTU_17_04:=http://cdimage.ubuntu.com/xubuntu/releases/17.04/release/xubuntu-17.04-desktop-amd64.iso

UBUNTU_16_04_3_IMG:=images/$(notdir $(UBUNTU_16_04_3))
UBUNTU_17_04_IMG:=images/$(notdir $(UBUNTU_17_04))
XUBUNTU_16_04_1_IMG:=images/$(notdir $(XUBUNTU_16_04_1))
XUBUNTU_17_04_IMG:=images/$(notdir $(XUBUNTU_17_04))

#IMAGE_FILES:=$(UBUNTU_16_04_3_IMG) $(UBUNTU_17_04_IMG) $(XUBUNTU_16_04_1_IMG) $(XUBUNTU_17_04_IMG)
IMAGE_FILES:=$(UBUNTU_16_04_3_IMG) $(XUBUNTU_16_04_1_IMG)

all: make_images

make_images: $(addsuffix _build,$(IMAGE_FILES))

$(UBUNTU_16_04_3_IMG)_build:
	python2 respin.py $(UBUNTU_16_04_3) gpdpocket-gnome-config

#$(UBUNTU_17_04_IMG)_build:
#	python2 respin.py $(UBUNTU_17_04)

$(XUBUNTU_16_04_1_IMG)_build:
	python2 respin.py $(XUBUNTU_16_04_1) gpdpocket-xfce-config

#$(XUBUNTU_17_04_IMG)_build:
#	python2 respin.py $(XUBUNTU_17_04) gpdpocket-xfce-config
