import os
import urllib.request
import importlib.util
import sys
import shutil

if os.name == "posix":
    if not os.access("/usr", os.W_OK):
        print("--!> /usr is not writeable, run as root")
        exit(1)
    instype = input("--?> Install from binary? [Y/n] ").lower() == "n"
    if instype:
        if os.system("git --version > /dev/null") != 0:
            print("--!> Git is not installed")
            exit(1)

        if importlib.util.find_spec("PyInstaller") is None:
            print("--!> PyInstaller is not installed, run `pip install pyinstaller` as root")
            exit(1)
        
        if os.system("make --version > /dev/null") != 0:
            print("--!> Make is not installed")
            exit(1)

        if os.path.isfile("/tmp/qolang"):
            print("---> Removing /tmp/qolang")
            os.remove("/tmp/qolang")
        if os.path.isdir("/tmp/qolang"):
            print("---> Removing /tmp/qolang")
            shutil.rmtree('/tmp/qolang')
        print("---> Cloning the git repository to /tmp/qolang")
        os.system("git clone https://github.com/QoLang/QoLang /tmp/qolang")
        print("---> Changing cwd to /tmp/qolang")
        os.chdir("/tmp/qolang")
        print("---> Running Makefile to build and install QoLang")
        os.system("make clean build install")
    else:
        if os.system("make --version > /dev/null") != 0:
            print("--!> Make is not installed")
            exit(1)

        if os.system("svn --version > /dev/null") != 0:
            print("--!> Subversion is not installed")
            exit(1)
        

        if os.path.isfile("/tmp/qolang"):
            print("---> Removing /tmp/qolang")
            os.remove("/tmp/qolang")
        if os.path.isdir("/tmp/qolang"):
            print("---> Removing /tmp/qolang")
            shutil.rmtree('/tmp/qolang')
        print("---> Creating /tmp/qolang")
        os.mkdir("/tmp/qolang")
        print("---> Changing cwd to /tmp/qolang")
        os.chdir("/tmp/qolang")
        print("---> Downloading Makefile")
        urllib.request.urlretrieve("https://raw.githubusercontent.com/QoLang/QoLang/master/Makefile", "Makefile")
        print("---> Creating /tmp/qolang/dist")
        os.mkdir("dist")
        print("---> Downloading QoLang binary")
        urllib.request.urlretrieve("https://github.com/QoLang/QoLang/releases/latest/download/qo", "dist/qo")
        print("---> Downloading built-in libraries")
        os.system("svn export https://github.com/QoLang/QoLang/trunk/libs")
        print("---> Running make to install QoLang")
        os.system("make install")
        print("---> Removing /tmp/qolang")
        shutil.rmtree('/tmp/qolang')
        print("---> Done!")

elif os.name == "nt":
    print("Windows is not supported yet. Please follow the instructions on the website.")
    exit(1)
else:
    print("Your operating system is not supported yet. Please follow the instructions on the website.")
    exit(1)
