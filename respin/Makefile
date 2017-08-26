UBUNTU_16_04_3:=http://releases.ubuntu.com/16.04/ubuntu-16.04.3-desktop-amd64.iso
UBUNTU_17_04:=http://releases.ubuntu.com/17.04/ubuntu-17.04-desktop-amd64.iso
XUBUNTU_16_04_3:=http://cdimage.ubuntu.com/xubuntu/releases/16.04/release/xubuntu-16.04.3-desktop-amd64.iso
XUBUNTU_17_04:=http://cdimage.ubuntu.com/xubuntu/releases/17.04/release/xubuntu-17.04-desktop-amd64.iso
MINT_18_2_XFCE:=http://mirror.netcologne.de/linuxmint/iso/stable/18.2/linuxmint-18.2-xfce-64bit.iso
MINT_18_2_CINNAMON:=http://mirror.netcologne.de/linuxmint/iso/stable/18.2/linuxmint-18.2-cinnamon-64bit.iso
LUBUNTU_17_04:=http://cdimage.ubuntu.com/lubuntu/releases/17.04/release/lubuntu-17.04-desktop-amd64.iso
LUBUNTU_16_04_3:=http://cdimage.ubuntu.com/lubuntu/releases/16.04.3/release/lubuntu-16.04.3-desktop-amd64.iso

UBUNTU_16_04_3_IMG:=images/$(notdir $(UBUNTU_16_04_3))
UBUNTU_17_04_IMG:=images/$(notdir $(UBUNTU_17_04))
XUBUNTU_16_04_3_IMG:=images/$(notdir $(XUBUNTU_16_04_3))
XUBUNTU_17_04_IMG:=images/$(notdir $(XUBUNTU_17_04))
MINT_18_2_XFCE_IMG:=images/$(notdir $(MINT_18_2_XFCE))
MINT_18_2_CINNAMON_IMG:=images/$(notdir $(MINT_18_2_CINNAMON))
LUBUNTU_17_04_IMG:=images/$(notdir $(LUBUNTU_17_04))
LUBUNTU_16_04_3_IMG:=images/$(notdir $(LUBUNTU_16_04_3))

IMAGE_FILES:=$(UBUNTU_16_04_3_IMG) $(UBUNTU_17_04_IMG) $(XUBUNTU_16_04_3_IMG) $(XUBUNTU_17_04_IMG)

all: make_images

make_images: $(addsuffix _build,$(IMAGE_FILES))

$(UBUNTU_16_04_3_IMG)_build:
	python2 respin.py $(UBUNTU_16_04_3) gpdpocket-gnome-config

$(UBUNTU_17_04_IMG)_build:
	python2 respin.py $(UBUNTU_17_04) gpdpocket-gnome-config

$(MINT_18_2_CINNAMON_IMG)_build:
	python2 respin.py $(MINT_18_2_CINNAMON) gpdpocket-gnome-config

$(XUBUNTU_16_04_3_IMG)_build:
	python2 respin.py $(XUBUNTU_16_04_3) gpdpocket-xfce-config

$(XUBUNTU_17_04_IMG)_build:
	python2 respin.py $(XUBUNTU_17_04) gpdpocket-xfce-config

$(MINT_18_2_XFCE_IMG)_build:
	python2 respin.py $(MINT_18_2_XFCE) gpdpocket-xfce-config	

$(LUBUNTU_17_04_IMG)_build:
	python2 respin.py $(LUBUNTU_17_04)

$(LUBUNTU_16_04_3_IMG)_build:
	python2 respin.py $(LUBUNTU_16_04_3)
