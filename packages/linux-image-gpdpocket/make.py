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
    templates = os.path.abspath("files/templates.tar.bz2")
    versionPrefix = ".1"
    variables = {
        "architecture": "amd64",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "linux-image",
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

print "extract templates"
templates = tarfile.open(config.templates, "r")
templates.extractall(config.temp)

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

print "fixing firmware directory"
shutil.move(config.build + "/lib/firmware", config.build + "/lib/" + versions[0])
os.makedirs(config.build + "/lib/firmware")
shutil.move(config.build + "/lib/" + versions[0], config.build + "/lib/firmware")

print "constructing control file"
control = open(config.temp + "/control", "rb").read()
variables = config.variables
variables["versionName"] = versions[0]
variables["versionCode"] = "-".join(versions[0].split("-")[:-1]) + config.versionPrefix

fp = open(config.manifest + "/control", "wb")
fp.write(control.format(**variables))
fp.flush()
fp.close()

print "constructing script files"
for script in ["/postinst", "/postrm", "/preinst", "/prerm"]:
    print ">> write debian%s" % (script)
    filepath = config.manifest + script
    content = open(config.temp + script, "rb").read()
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
