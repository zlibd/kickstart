# Kickstart
Fedora Workstation Kickstart Script and Files

# Overview

This is part of a personal goal to try and automate the installation and post-installation process and to keep up with how I modify my system.  

## `kickstart.py`
Python script that reads from `secrets.py` and substitutes the provided infromation into the Kickstart file. It will start a python HTTP server to allow for your installation media to pull the modified Kickstart file and proceed with the setup. The python HTTP server currently will give a `404` HTTP status code for any requests other than the Kickstart file explicitly stated in the `secrets.py`.

The intent is to easily pass sensitive information into a generally accessible Kickstart file. 

## `secrets.py`
The example file `secrets.example.py` can be used by copying or renaming to `secrets.py`.  

```
LISTEN_ADDR = "0.0.0.0"
LISTEN_PORT = 8080
KICKSTART_FILE = "example.ks"
USER_NAME = "user"
USER_PASS = "password"
FDE_PASS = "fde123"
HOST_NAME = "localhost"
```

`LISTEN_ADDR` is the address to listen on for the python HTTP server.  By default it is set globally, and it is likely not necessary to change.  
`LISTEN_PORT` is the port to listen on for the python HTTP server.  By default it is set to `8080`, but can be changed as necessary.  
`KICKSTART_FILE` is the file you want to use to substitute the sensitive information into and serve via the python HTTP server.  
`USER_NAME` is the username to pass into the Kickstart file.  
`USER_PASS` is the password to pass into the Kickstart file.  `kickstart.py` will salt and convert the password into an MD5 hash before passing into the Kickstart file.  
`FDE_PASS` is the ***OPTIONAL*** full-disk encryption password for the Kickstart file.  If a password is not provided, the options will not be passed into the Kickstart file.  If the password is provided, the options `--encrypted --luks-version=luks2 --passphrase=` will be passed into the Kickstart file.  
`HOST_NAME` is the device name to pass into the Kickstart file.
`BOOTLOADER_PASS` is the ***OPTIONAL*** password protection for grub.

## `fedora.ks`
My current work-in-progress Kickstart file. This will automate the installation of my system, to include things like full-disk encryption and package installation.  This will also run standalone bash scripts in the `scripts` folder as a post-installation task. This is done to keep things modular and the Kickstart file clean.

# Requirements:
* Webserver with Python 3.5+ to host the Kickstart file.
  * This can be any spare computer/VM that is accessible by the workstation installing Fedora.
* If using my Kickstart file, currently needs to have an Ethernet connection.

# Use:
* Clone this repository:  
`git clone https://github.com/dirwalk/Kickstart.git`  
`cd Kickstart`
* Copy or rename the `secrets.example.py` to `secrets.py`.
    * Copy:
      * `cp secrets.example.py secrets.py`
    * Rename:
      * `mv secrets.example.py secrets.py`
* Modify the variables in `secrets.py`.
  * LISTEN_ADDR
    * `sed -i 's/0.0.0.0/NEW_IP/' secrets.py`
  * LISTEN_PORT
    * `sed -i 's/8080/NEW_PORT/' secrets.py`
  * KICKSTART_FILE
    * `sed -i 's/example.ks/NEW_KICKSTART/' secrets.py`
  * USER_NAME
    * `sed -i 's/user/NEW_USER/' secrets.py`
  * USER_PASS
    * `sed -i 's/password/NEW_PASSWORD/' secrets.py`
  * FDE_PASS
    * `sed -i 's/fde123/NEW_FDE/' secrets.py`
  * HOST_NAME  
    * `sed -i 's/localhost/NEW_HOSTNAME/' secrets.py`
  * BOOTLOADER_PASS
    * `sed -i 's/bootloader/NEW_BOOTLOADER/' secrets.py`
* Run `kickstart.py` to pass into your Kickstart file and run the python HTTP server.  
`python3 kickstart.py`
* At boot screen of Fedora's installation media, press TAB and append ***BEFORE*** `quiet`.  
`inst.ks=http://<SERVER_IP>:<PORT>/<KICKSTART_FILE>`
* Press enter and the installation will proceed. 