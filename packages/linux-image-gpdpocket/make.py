import shutil
import subprocess
import os
import tarfile

class Config(object):
    build = os.path.abspath("build")
    output = os.path.abspath("output")
    manifest = os.path.abspath("build/DEBIAN")
    temp = os.path.abspath("tmp")
    kernel = os.path.abspath("files/bootstrap-kernel-boot.tar.bz2")
    modules = os.path.abspath("files/bootstrap-kernel-lib.tar.bz2")
    templates = os.path.abspath("files/DEBIAN")
    versionPrefix = ".1"
    variables = {
        "architecture": "amd64",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "linux-image-gpdpocket",
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

print "extract kernel"
kernel = tarfile.open(config.kernel, "r")
kernel.extractall(config.build)
images = filter(lambda x: x.startswith("vmlinuz"), [os.path.basename(m.name) for m in kernel.members])
print ">> extracted images: %s" % (", ".join(images))
assert(len(images) == 1)

print "extract modules"
modules = tarfile.open(config.modules, "r")
modules.extractall(config.build)
versions = [x[1] for x in filter(lambda x: x[0] == 'lib/modules', [(os.path.dirname(m.name), os.path.basename(m.name)) for m in modules.members])]
print ">> found kernel versions: %s" % (", ".join(versions))
assert(len(versions) == 1)

print "patching brcmfmac4356 firmware"
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
control = open(config.templates + "/control", "rb").read()
variables = config.variables
variables["versionName"] = versions[0]
variables["versionCode"] = "-".join(versions[0].split("-")[:-1]) + config.versionPrefix

fp = open(config.manifest + "/control", "wb")
fp.write(control.format(**variables))
fp.flush()
fp.close()

print "constructing script files"
for script in ["/postinst", "/postrm", "/preinst", "/prerm"]:
    print ">> write DEBIAN%s" % (script)
    filepath = config.manifest + script
    content = open(config.templates + script, "rb").read()
    fp = open(filepath, "wb")
    fp.write(content.replace("__VERSION_CODE__", variables["versionName"]))
    fp.flush()
    fp.close()
    os.chmod(filepath, 0555)

print "building binary package"
command = ["dpkg-deb", "-b", config.build]
command.append("%s/%s-%s.deb" % (config.output, variables["name"], variables["versionName"]))
subprocess.call(command)

print "done"
