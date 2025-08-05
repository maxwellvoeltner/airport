PYTHON_VERSION = 3
PROJECT_NAME = puppetmaster
VIRTUAL_ENV = virtualenv
ARCHITECTURE = $(shell dpkg --print-architecture)
LOCAL_IP = $(shell hostname -I | awk '{print $$1}')
PYINSTALLER = pyinstaller
VERSION_FILE := VERSION.txt
VERSION := $(shell cat ${VERSION_FILE})
UNAME_S := $(shell uname -s)
RM := /bin/rm -rf 	
PYTHON := ./$(VIRTUAL_ENV)/bin/python3
PIP := ./$(VIRTUAL_ENV)/bin/pip3
VENV := python$(PYTHON_VERSION) -m venv
LOCAL_PIP := pip$(PYTHON_VERSION)

develop:
	sudo apt update && sudo apt install software-properties-common -y

	sudo apt-get -y install python$(PYTHON_VERSION)-venv libdbus-glib-1-dev libssl-dev libssh2-1-dev \
							libbluetooth-dev python3-dev libcairo2-dev libgirepository1.0-dev libbluetooth-dev \
							libdbus-1-dev bluez-tools python3-cairo-dev python$(PYTHON_VERSION)-dev \
							libboost-python-dev libboost-thread-dev libsqlite3-dev 
	sudo apt install -y python3-pip python3-dev libcairo2-dev libgirepository1.0-dev \
                 	 libbluetooth-dev libdbus-1-dev bluez-tools python3-cairo-dev \
                 	 rfkill meson patchelf bluez ubertooth adb python-is-python3
	$(VENV) $(VIRTUAL_ENV)
	$(PIP) install -Ur requirements.txt
	$(LOCAL_PIP) install -r requirements.txt
	$(PIP) install bump2version==1.0.1
	$(PIP) install setuptools==70.1.0  
	$(LOCAL_PIP) install bump2version==1.0.1 
	$(LOCAL_PIP) install setuptools==70.1.0 