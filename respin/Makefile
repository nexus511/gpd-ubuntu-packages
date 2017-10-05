UBUNTU_16_04_3:=http://releases.ubuntu.com/16.04/ubuntu-16.04.3-desktop-amd64.iso|gpdpocket-gnome-config
UBUNTU_17_04:=http://releases.ubuntu.com/17.04/ubuntu-17.04-desktop-amd64.iso|gpdpocket-gnome-config
XUBUNTU_16_04_3:=http://cdimage.ubuntu.com/xubuntu/releases/16.04/release/xubuntu-16.04.3-desktop-amd64.iso|gpdpocket-xfce-config
XUBUNTU_17_04:=http://cdimage.ubuntu.com/xubuntu/releases/17.04/release/xubuntu-17.04-desktop-amd64.iso|gpdpocket-xfce-config
MINT_18_2_XFCE:=http://mirror.netcologne.de/linuxmint/iso/stable/18.2/linuxmint-18.2-xfce-64bit.iso|
MINT_18_2_CINNAMON:=http://mirror.netcologne.de/linuxmint/iso/stable/18.2/linuxmint-18.2-cinnamon-64bit.iso|
LUBUNTU_17_04:=http://cdimage.ubuntu.com/lubuntu/releases/17.04/release/lubuntu-17.04-desktop-amd64.iso|
LUBUNTU_16_04_3:=http://cdimage.ubuntu.com/lubuntu/releases/16.04.3/release/lubuntu-16.04.3-desktop-amd64.iso|
UBUNTU_GNOME_16.04.3:=http://cdimage.ubuntu.com/ubuntu-gnome/releases/16.04/release/ubuntu-gnome-16.04.3-desktop-amd64.iso|gpdpocket-gnome-config
UBUNTU_GNOME_17.04:=http://cdimage.ubuntu.com/ubuntu-gnome/releases/17.04/release/ubuntu-gnome-17.04-desktop-amd64.iso|gpdpocket-gnome-config

remove_target_part = $(patsubst %.sync,%,$(patsubst %.target,%,$1))
get_target_dist = $(word 1,$(subst -, ,$1))

output_file_name = output/$(call remove_target_part,$1)_gpdpocket_$(TIMESTAMP).iso
target_url = $(filter %/$(call remove_target_part,$1).iso,$(IMAGES))
sync_directory = htdocs/iso/$(call get_target_dist,$1)/$(TIMESTAMP)/
target_name = $(patsubst %.iso,%.target,$(notdir $1))
get_image_part = $(word 1,$(subst |, ,$1))
get_additions = $(subst ;, ,$(word 2,$(subst |, ,$(filter $(call remove_target_part,$1).iso|%,$(ADDITIONS)))))

define lock_call
  touch $(1) ; flock $(1) -c "$(2)"
endef

ELEMENTS:=$(UBUNTU_16_04_3) $(UBUNTU_17_04) \
	$(XUBUNTU_16_04_3) $(XUBUNTU_17_04) \
	$(MINT_18_2_XFCE) $(MINT_18_2_CINNAMON) \
	$(LUBUNTU_17_04) $(LUBUNTU_16_04_3) \
	$(UBUNTU_GNOME_16.04.3) $(UBUNTU_GNOME_17.04)

IMAGES:=$(foreach element,$(ELEMENTS),$(call get_image_part,$(element)))
ADDITIONS:=$(foreach element,$(ELEMENTS),$(notdir $(element)))
TARGETS:=$(foreach image,$(IMAGES),$(call target_name,$(image)))
SYNC_TARGETS:=$(patsubst %.target,%.sync,$(TARGETS))
TIMESTAMP:=$(shell TZ=UTC date --iso)

list_targets:
	$(info supported targets:)
	$(foreach target,$(TARGETS),$(info :     $(target)))
	$(info suported syncs:)
	$(foreach target,$(SYNC_TARGETS),$(info :     $(target)))

all: make_images

sync_images: $(SYNC_TARGETS)

make_images: $(TARGETS)

%.target:
	$(call lock_call,build.lock,python2 respin.py $(call target_url,$@) $(call output_file_name,$@) $(call get_additions,$@))

output/%_gpdpocket_$(TIMESTAMP).iso:
	make -j1 TIMESTAMP=$(TIMESTAMP) "$*.target"

%.sync: $(call output_file_name,%)
	ssh nexus511.repo "mkdir -p $(call sync_directory,$@)"
	$(call lock_call,upload.lock,scp $(call output_file_name,$@) nexus511.repo:$(call sync_directory,$@))
	rm $(call output_file_name,$@)
