import shutil
import subprocess
import os
import tarfile

class Config(object):
    build = os.path.abspath("build")
    files = os.path.abspath("files")
    output = os.path.abspath("output")
    manifest = os.path.abspath("build/DEBIAN")
    datafile = os.path.abspath("files/data.tar.gz")
    temp = os.path.abspath("tmp")
    templates = os.path.abspath("files/DEBIAN")
    version = "1.999.0-gpdpocket"
    variables = {
        "architecture": "all",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "linux-firmware",
    }

print "first we cleanup our stuff"
config = Config()
for rdir in [config.build, config.temp, config.output]:
    try:
        print ">> remove %s" % (rdir)
        shutil.rmtree(rdir)
    except:
        pass

print "create directories"
os.makedirs(config.temp)
os.makedirs(config.output)
os.makedirs(config.build)
os.makedirs(config.manifest)

print "unpacking firmware archive"
datafile = tarfile.open(config.datafile, "r")
datafile.extractall(config.build)

print "copy brcmfmac4356 firmware"
copylist = [
    ( 'files/brcmfmac4356-pcie.bin', '/lib/firmware/brcm/brcmfmac4356-pcie.bin', 0644 ),
    ( 'files/brcmfmac4356-pcie.txt', '/lib/firmware/brcm/brcmfmac4356-pcie.txt', 0644 ),
]

for src, dst, mode in copylist:
    print ">> copy (0%o) %s" % (mode, dst)
    src = os.path.abspath(src)
    dst = config.build + dst
    dn = os.path.dirname(dst)
    if not os.path.isdir(dn):
        os.makedirs(dn)
    shutil.copy(src, dst)
    os.chmod(dst, mode)

print "constructing control file"
variables = config.variables
variables["version"] = config.version
control = open(config.files + "/DEBIAN/control", "rb").read()
fp = open(config.manifest + "/control", "wb")
fp.write(control.format(**variables))
fp.flush()
fp.close()

print "constructing script files"
for script in ["/postinst"]:
    print ">> write DEBIAN%s" % (script)
    filepath = config.manifest + script
    content = open(config.templates + script, "rb").read()
    fp = open(filepath, "wb")
    fp.write(content.replace("__VERSION_CODE__", variables["version"]))
    fp.flush()
    fp.close()
    os.chmod(filepath, 0555)

print "building binary package"
command = ["fakeroot", "dpkg-deb", "-b", config.build]
command.append("%s/%s-%s.deb" % (config.output, variables["name"], variables["version"]))
subprocess.call(command)

print "done"
