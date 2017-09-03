import shutil
import subprocess
import os
import tarfile
import sys

class Config(object):
    build = os.path.abspath("build")
    output = os.path.abspath("output")
    manifest = os.path.abspath("build/DEBIAN")
    temp = os.path.abspath("tmp")
    templates = os.path.abspath("files/DEBIAN")
    prebuilt = os.path.abspath("../prebuilt/output/")
    variables = {
        "architecture": "amd64",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "linux-image-generic",
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

print "aquire packaghes from prebuilt"
image = filter(lambda x: x.startswith("linux-image") and x.find("-extra-") < 0, os.listdir(config.prebuilt))
if len(image) != 1:
    print "ERROR: need exactly one kernel version. please cleanup and rebuild packages/prebuilt"
    sys.exit(1)
image = image[0]

extra = filter(lambda x: x.startswith("linux-image") and x.find("-extra-") > 0, os.listdir(config.prebuilt))
if len(extra) != 1:
    print "ERROR: need exactly one kernel extra version. please cleanup and rebuild packages/prebuilt"
    sys.exit(1)
extra = extra[0]

print "found kernel package %s:" % (image)
linux_image_package, version, ext = image.split("_")
linux_extra_package, _, _ = extra.split("_")

print "  version: %s" % (version)
print "  package: %s" % (linux_image_package)
print "  extra:   %s" % (linux_extra_package)


print "constructing control file"
variables = config.variables
variables["linux-image-package"] = linux_image_package
variables["linux-extra-package"] = linux_extra_package
variables["version"] = version
control = open(config.templates + "/control", "rb").read()

fp = open(config.manifest + "/control", "wb")
fp.write(control.format(**variables))
fp.flush()
fp.close()

print "building binary package"
command = ["fakeroot", "dpkg-deb", "-b", config.build]
command.append("%s/%s-%s.deb" % (config.output, variables["name"], variables["version"]))
subprocess.call(command)

print "done"
