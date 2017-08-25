# gpd-ubuntu-packages
This repository shall provide the base for building ubuntu packages from most of the patches currently used to get linux on the gpd-pocket.

This is still work in progress. For more information visit https://apt.nexus511.net/ .

# Note
This is work in process and will be basically be build on https://github.com/cawilliamson/ansible-gpdpocket .

# Required packages

To properly build the packages you need

- dpkg-sig
- dpkg-dev
- syslinux-utils
- isolinux
- xorriso

To build the kernel you will also need

- libelf-dev
- build-essential
- libssl-dev

to be installed.


