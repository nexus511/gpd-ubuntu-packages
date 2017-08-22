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
    version = "0.0.2"
    variables = {
        "architecture": "all",
        "maintainer": "Falk Garbsch <github.com@cyberstalker.eu>",
        "name": "gpdpocket-power",
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
copylist = [
    ( 'files/gpd-fan.conf', '/etc/gpd/fan.conf', 0644 ),
    ( 'files/gpd-fan.py', '/usr/local/sbin/gpd-fan', 0755 ),
    ( 'files/gpd-fan.service', '/etc/systemd/system/gpd-fan.service', 0644 ),
    ( 'files/gpd-fan.sh', '/lib/systemd/system-sleep/gpd-fan', 0755 ),
    ( 'files/tlp', '/etc/default/tlp', 0644 )
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
src = "/etc/systemd/system/gpd-fan.service"
dst = config.build + "/etc/systemd/system/basic.target.wants/gpd-fan.service"
dn = os.path.dirname(dst)
if not os.path.exists(dst):
    os.makedirs(dn)
os.symlink(src, dst)

print "create blacklist item"
blacklist = config.build + "/etc/pm/config.d/brcmfmac"
dn = os.path.dirname(blacklist)
if not os.path.isdir(dn):
    os.makedirs(dn)
fp = open(blacklist, "wb")
fp.write("SUSPEND_MODULES=\"brcmfmac\"\n")
fp.flush()
fp.close()

print "write control"
variables = config.variables
variables["version"] = config.version
control = open(config.files + "/DEBIAN/control", "rb").read()
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
    fp.write(content.replace("__VERSION_CODE__", variables["version"]))
    fp.flush()
    fp.close()
    os.chmod(filepath, 0555)

print "building binary package"
command = ["fakeroot", "dpkg-deb", "-b", config.build]
command.append("%s/%s-%s.deb" % (config.output, variables["name"], variables["version"]))
subprocess.call(command)

print "done"
