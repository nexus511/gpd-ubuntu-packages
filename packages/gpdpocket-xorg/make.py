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
    version = "0.0.1"
    variables = {
        "architecture": "all",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "gpdpocket-xorg",
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

print "setup device rotation"
copylist = [
    ('files/rotate/01gpd-rotate', '/etc/X11/Xsession.d/01gpd-rotate', 0755),
    ('files/rotate/01gpd-rotate', '/etc/X11/xinit/xinitrc.d/01gpd-rotate', 0755 ),
    ('files/rotate/gpd-rotate.conf', '/etc/gpd/rotate.conf', 0644 ),
    ('files/rotate/gpd-rotate.py', '/usr/local/sbin/gpd-rotate', 0755 ),
    ('files/rotate/gpd-rotate.service', '/etc/systemd/system/gpd-rotate.service', 0644 )
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

print "setup xorg configuration"
copylist = [
    ( 'files/config/20-intel.conf', '/etc/X11/xorg.conf.d/20-intel.conf', 0644 )
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

print "enable systemd service"
src = "/etc/systemd/system/gpd-rotate.service"
dst = config.build + "/etc/systemd/system/multi-user.target.wants/gpd-rotate.service"
dn = os.path.dirname(dst)
if not os.path.exists(dst):
    os.makedirs(dn)
os.symlink(src, dst)

print "write control"
variables = config.variables
variables["version"] = config.version
control = open(config.files + "/DEBIAN/control", "rb").read()
fp = open(config.manifest + "/control", "wb")
fp.write(control.format(**variables))
fp.flush()
fp.close()

print "building binary package"
command = ["dpkg-deb", "-b", config.build]
command.append("%s/%s-%s.deb" % (config.output, variables["name"], variables["version"]))
subprocess.call(command)

print "done"
