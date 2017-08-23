import os
import sys
import shutil
import subprocess
import traceback

class Config(object):
	def __init__(self, args):
		self.image_dir = os.path.abspath("./images")
		self.tmp_dir = os.path.abspath("./tmp")
		self.output_dir = os.path.abspath("./output")

		self.url = args[1]
		self.name = os.path.basename(self.url)
		
		self.image = self.image_dir + "/" + self.name
		self.output = self.output_dir + "/" + self.name
		self.tmp = self.tmp_dir + "/" + self.name
		self.mount_iso = self.tmp + "/mnt/iso"
		self.clone_iso = self.tmp + "/data/iso"
		self.mount_squashfs = self.tmp + "/mnt/squashfs"
		self.clone_squashfs = self.tmp + "/data/squashfs"
		self.squashfs_path = self.clone_iso + "/casper/filesystem.squashfs"
		self.squashfs_sig = self.clone_iso + "/casper/filesystem.squashfs.gpg"
		self.squashfs_manifest = self.clone_iso + "/casper/filesystem.squashfs.manifest"

		self.pseudo_fs = ["/dev", "/dev/pts", "/proc", "/sys"]
		self.repo_base = os.path.abspath("../repo")
		self.repo = self.repo_base + "/dists/stable/main/binary"
		self.keyfile = self.repo_base + "/keyFile"
		self.root = self.clone_squashfs

		self.packages = ["gpdpocket", "gpdpocket-xfce-config"]
		self.hybridboot = "/usr/lib/ISOLINUX/isohdpfx.bin"
		self.volname = "gpdpocket"
		self.initramfs_modules = [ "btusb", "loop", "overlay", "pwm-lpss", "pwm-lpss-platform", "squashfs" ]

def clone_image(src, mnt, dst):
	print ">> mount %s -> %s" % (src, mnt)
	command = ["mount", "-o", "loop", src, mnt]
	assert(subprocess.call(command) == 0)

	print ">> rsync %s -> %s" % (mnt, dst)
	command = ["rsync", "-a", mnt + "/.", dst]
	assert(subprocess.call(command) == 0)

	print ">> umount %s" % (mnt)
	command = ["umount", mnt]
	assert(subprocess.call(command) == 0)

config = Config(sys.argv)

print "cleanup %s" % (config.tmp)
try:
	shutil.rmtree(config.tmp)
except:
	pass

if os.path.exists(config.output):
	print "remove %s" % (config.output)
	os.remove(config.output)

print "make directories"
for dn in [config.mount_iso, config.mount_squashfs, config.clone_iso, config.clone_squashfs, config.image_dir, config.output_dir]:
	print ">> mkdir %s" % (dn)
	if not os.path.isdir(dn):
		os.makedirs(dn)

# TODO: add downloading here

print "extract files from iso"
clone_image(config.image, config.mount_iso, config.clone_iso)

print "extract files from squashfs"
clone_image(config.squashfs_path, config.mount_squashfs, config.clone_squashfs)

print "remove original squashfs file and metadata"
for fn in [config.squashfs_path, config.squashfs_manifest, config.squashfs_sig]:
	print ">> rm %s" % (fn)
	if os.path.exists(fn):
		os.remove(fn)

print "mount pseudo filesystems"
for fs in config.pseudo_fs:
	print ">> mount %s" % (fs)
	command = ["mount", "--bind", fs, config.root + fs]
	assert(subprocess.call(command) == 0)

try:
	print "backup some files"
	shutil.move(config.root + "/etc/resolv.conf", config.root + "/etc/resolv.conf.distrib")
	shutil.copy(config.root + "/etc/apt/sources.list", config.root + "/etc/apt/sources.list.distrib")
	shutil.copy(config.root + "/etc/initramfs-tools/modules", config.root + "/etc/initramfs-tools/modules.distrib")

	print "update target configuration"
	shutil.copy("/etc/resolv.conf", config.root + "/etc/resolv.conf")
	fp = open(config.root + "/etc/initramfs-tools/modules", "a")
	fp.write("\n".join(config.initramfs_modules) + "\n")
	fp.flush()
	fp.close()

	print "clone repository to target and activate it"
	command = ["rsync", "-va", config.repo + "/.", config.root + "/tmp/repo"]
	assert(subprocess.call(command) == 0)
	shutil.copy(config.keyfile, config.root + "/tmp/repo/keyFile")

	print "activate repository on target"
	command = ["chroot", config.root, "apt-key", "add", "/tmp/repo/keyFile"]
	assert(subprocess.call(command) == 0)
	fp = open(config.root + "/etc/apt/sources.list", "a")
	fp.write("deb file:///tmp/repo /\n")
	fp.write("deb http://de.archive.ubuntu.com/ubuntu/ xenial universe\n")
	fp.flush()
	fp.close()
	command = ["chroot", config.root, "apt", "update"]
	assert(subprocess.call(command) == 0)

	print "install the gpdpocket packages"
	command = ["chroot", config.root, "apt", "-y", "install"]
	command += config.packages
	assert(subprocess.call(command) == 0)

	print "restore target configuration"
	shutil.move(config.root + "/etc/apt/sources.list.distrib", config.root + "/etc/apt/sources.list")
	shutil.move(config.root + "/etc/initramfs-tools/modules.distrib", config.root + "/etc/initramfs-tools/modules")

	print "ensure that gpdpocket repo is left behind"
	fp = open(config.root + "/etc/apt/sources.list", "a")
	fp.write("# gpdpocket packages")
	fp.write("deb https://apt.nexus511.net/repo/dists/stable/main/binary /\n")
	fp.flush()
	fp.close()
	command = [ "chroot", config.root, "apt", "update" ]
	assert(subprocess.call(command) == 0)

	print "restore target configuration"
	shutil.move(config.root + "/etc/resolv.conf.distrib", config.root + "/etc/resolv.conf")

	print "unmount pseudo filesystems"
	for fs in reversed(config.pseudo_fs):
		print ">> umount %s" % (fs)
		command = ["umount", config.root + fs]
		subprocess.call(command)

	print "write metadata to %s" % (config.squashfs_manifest)
	command = [ "chroot", config.root, "dpkg-query", "-W", "--showformat='${Package} ${Version}\n'" ]
	data = subprocess.check_output(command)
	fp = open(config.squashfs_manifest, "wb")
	fp.write(data)
	fp.flush()
	fp.close()

except:
	traceback.print_exc()
	print "unmount pseudo filesystems"
	for fs in reversed(config.pseudo_fs):
		print ">> umount %s" % (fs)
		command = ["umount", config.root + fs]
		subprocess.call(command)
	sys.exit(1)

print "clone updated kernel to iso"
shutil.copy(config.root + "/vmlinuz", config.clone_iso + "/casper/vmlinuz.efi")
shutil.copy(config.root + "/initrd.img", config.clone_iso + "/casper/initrd.lz")

print "collect filesystem size"
command = "du -sx --block-size=1 %s | cut -f1" % (config.root)
data = subprocess.check_output(command, shell = True)
fp = open(config.clone_iso + "/casper/filesystem.size", "wb")
fp.write("%s\n" % data)
fp.flush()
fp.close()

print "repack squashfs to %s" % (config.squashfs_path)
command = [ "mksquashfs", config.root, config.squashfs_path, "-comp", "xz" ]
assert(subprocess.call(command) == 0)

print "collect md5 hashes"
command = "cd %s ; find . -type f -print0 | xargs -0 md5sum" % (config.clone_iso)
data = subprocess.check_output(command, shell = True)
fp = open(config.root + "/md5sum.txt", "wb")
fp.write(data)
fp.flush()
fp.close()

print "create new iso image based on updated squashfs"
pwd = os.path.abspath(".")
os.chdir(config.clone_iso)
command = [
	"xorriso",
	"-as", "mkisofs",
	"-iso-level", "3",
	"-full-iso9660-filenames",
	"-volid", config.volname,
	"-isohybrid-mbr", config.hybridboot,
	"-eltorito-boot", "isolinux/isolinux.bin",
	"-no-emul-boot",
	"-eltorito-catalog", "isolinux/boot.cat",
	"-no-emul-boot",
	"-boot-load-size", "4"
	"-boot-info-table",
	"-eltorito-alt-boot",
	"-e", "boot/grub/efi.img",
	"-no-emul-boot",
	"-isohybrid-gpt-basdat",
	"-o", config.output,
	"."
]
assert(subprocess.call(command) == 0)
os.chdir(pwd)


