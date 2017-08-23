UBUNTU_16_04_3:=http://releases.ubuntu.com/16.04/ubuntu-16.04.3-desktop-amd64.iso
UBUNTU_17_04:=http://releases.ubuntu.com/17.04/ubuntu-17.04-desktop-amd64.iso
XUBUNTU_16_04_1:=http://cdimage.ubuntu.com/xubuntu/releases/16.04/release/xubuntu-16.04.1-desktop-amd64.iso
XUBUNTU_17_04:=http://cdimage.ubuntu.com/xubuntu/releases/17.04/release/xubuntu-17.04-desktop-amd64.iso

UBUNTU_16_04_3_IMG:=images/$(notdir $(UBUNTU_16_04_3))
UBUNTU_17_04_IMG:=images/$(notdir $(UBUNTU_17_04))
XUBUNTU_16_04_1_IMG:=images/$(notdir $(XUBUNTU_16_04_1))
XUBUNTU_17_04_IMG:=images/$(notdir $(XUBUNTU_17_04))

#SOURCE_FILES:=$(UBUNTU_16_04_3) $(UBUNTU_17_04) $(XUBUNTU_16_04_3) $(XUBUNTU_17_04)
IMAGE_FILES:=$(UBUNTU_16_04_3_IMG) $(UBUNTU_17_04_IMG) $(XUBUNTU_16_04_3_IMG) $(XUBUNTU_17_04_IMG)

all:

make_images: $(addsuffix _build,$(IMAGE_FILES))

$(UBUNTU_16_04_3_IMG)_build:
	make -f make/Respin.mk IMAGE_SOURCE=$(UBUNTU_16_04_3) respin

$(UBUNTU_17_04_IMG)_build:
	make -f make/Respin.mk IMAGE_SOURCE=$(UBUNTU_17_04) respin

$(XUBUNTU_16_04_1_IMG)_build:
	make -f make/Respin.mk IMAGE_SOURCE=$(XUBUNTU_16_04_1) respin

$(XUBUNTU_17_04_IMG)_build:
	make -f make/Respin.mk IMAGE_SOURCE=$(XUBUNTU_17_04) respin
