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
    WIN_QO = "C:\\qolang"

    if not os.access("C:\\", os.W_OK):
        print("--!> C:\\ is not writeable, run as root")
        exit(1)

    instype = input("--?> Install from git (requires git)? [Y/n] ").lower() != "n"

    if instype:
        if os.system("git --version") != 0:
            print("--!> Installing with git requires git, git is not installed")
            exit(1)

        if os.path.isdir(WIN_QO):
            print("---> Removing old qolang")
            try:
                shutil.rmtree(WIN_QO)
            except:
                print("--!> Failed to remove old qolang, delete it manually from", WIN_QO)
                exit(1)
                       
        print("---> Creating", WIN_QO)
        os.mkdir(WIN_QO)
        print("---> Cloning the git repository to", WIN_QO)
        os.system("git clone https://github.com/QoLang/QoLang "+WIN_QO)
        print("---> Downloading QoLang binary")
        urllib.request.urlretrieve(
            "https://github.com/QoLang/QoLang/releases/latest/download/qo.exe", WIN_QO+"\\qo.exe")

        print("---> Adding qolang to PATH")
        cmd = 'setx PATH "%PATH%;'+WIN_QO+'"'
        try:
            os.system(cmd)
        except:
            print("--!> Allready added to PATH, but if you want, run "+cmd)
        print("---> Done!")

    else:
        if os.path.isdir(WIN_QO):
            print("---> Removing old qolang")
            shutil.rmtree(WIN_QO)

        print("---> Creating", WIN_QO)
        os.mkdir(WIN_QO)
        print("---> Changing cwd to", WIN_QO)
        os.chdir(WIN_QO)
        print("---> Downloading QoLang binary")
        urllib.request.urlretrieve(
            "https://github.com/QoLang/QoLang/releases/latest/download/qo.exe", "qo.exe")

        # TODO: find alternative to svn
        print("---> Downloading built-in libraries")
        # os.system("svn export https://github.com/QoLang/QoLang/trunk/libs")

        print("--!> TODO: find alternative to svn. Skipping... So, you have to download the libs manually, and copy them to C:\\qolang\\libs")
        print("---> https://github.com/QoLang/QoLang/tree/master/libs")

        print("---> Adding qolang to PATH")
        cmd ="setx PATH \"%PATH%;"+WIN_QO+'"'
        try:
            os.system(cmd)
        except:
            print("--!> Allready added to PATH, but if you want, run "+cmd)
 
        print("---> Done!")

else:
    print("Your operating system is not supported yet. Please follow the instructions on the website.")
    print("https://qolang.camroku.tech/#Install")
    exit(1)
