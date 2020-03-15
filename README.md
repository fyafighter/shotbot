Shotbot is a Lacrosse goalie training system.

It runs on a raspberry pi and uses 3 docker containers: 
redis, api, and worker.

The default user on the raspberry pi is "pi" 
(naturally - however I write this down as I forgot it after not logging into the machine for 9 months after I set it up...)

1. Setup the raspberry pi.
https://www.raspberrypi.org/downloads/raspbian/

2. Install docker:
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker pi
newgrp docker

3. Install Docker Compose
sudo apt-get install libffi-dev libssl-dev
sudo apt-get install -y python python-pip
sudo apt-get remove python-configparser

Add vm.overcommit_memory = 1 to /etc/sysctl.conf

4. Checkout, build, and run
git clone https://github.com/fyafighter/shotbot.git
cd shotbot
docker-compose up --build

5. Download and install the app.
This can be done manually today by building and deploying from the flutter application. 
cd shotbot_app 
code .

TODO: Publish the app. 


DETAILS ON THE TARGETING SYSTEM
The Shotbot is setup on a 3x3 grid for targetting. The easiest way to get started is to start up the shotbot and the app, then center the system with the controls in the app, and then use the various shooting modes. 