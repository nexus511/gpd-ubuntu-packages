import shutil
import subprocess
import os
import tarfile

class Config(object):
    build = os.path.abspath("build")
    files = os.path.abspath("files")
    output = os.path.abspath("output")
    manifest = os.path.abspath("build/DEBIAN")
    temp = os.path.abspath("tmp")
    templates = os.path.abspath("files/DEBIAN")
    version = "0.1.0"
    variables = {
        "architecture": "all",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "gpdpocket-xfce-config",
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

print "copy files"
os.makedirs(config.build + "/etc/skel/.config")
shutil.copytree(config.files + "/xfce4", config.build + "/etc/skel/.config/xfce4")

print "write control"
variables = config.variables
variables["version"] = config.version
control = open(config.files + "/DEBIAN/control", "rb").read()
fp = open(config.manifest + "/control", "wb")
fp.write(control.format(**variables))
fp.flush()
fp.close()

print "building binary package"
command = ["fakeroot", "dpkg-deb", "-b", config.build]
command.append("%s/%s-%s.deb" % (config.output, variables["name"], variables["version"]))
subprocess.call(command)

print "done"
