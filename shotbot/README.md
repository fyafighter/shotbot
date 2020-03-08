Shotbot is a goalie training system.

It runs on a raspberry pi.

The default user on the raspberry pi is "pi" 
(naturally - however I write this down as I forgot it after not logging into the machine for 9 months after I set it up...)

1: Setup the raspberry pi.
install base os
(DETAILS)
install a bunch of packages
update the os

install docker:
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
newgrp docker

Install Docker Compose
sudo apt-get install libffi-dev libssl-dev
sudo apt-get install -y python python-pip
sudo apt-get remove python-configparser

Add vm.overcommit_memory = 1 to /etc/sysctl.conf
