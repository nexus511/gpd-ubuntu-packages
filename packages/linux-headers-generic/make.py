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
        "name": "linux-headers-generic",
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
headers = filter(lambda x: x.startswith("linux-headers") and x.find("-generic") > 0, os.listdir(config.prebuilt))
if len(headers) != 1:
    print "ERROR: need exactly one headers version. please cleanup and rebuild packages/prebuilt"
    sys.exit(1)
headers = headers[0]

print "found headers package %s:" % (headers)
linux_headers_package, version, ext = headers.split("_")

print "  version: %s" % (version)
print "  package: %s" % (linux_headers_package)


print "constructing control file"
variables = config.variables
variables["linux-headers-package"] = linux_headers_package
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
