#!/bin/bash

########### Installing Pre requisite###############
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce-18.09.0-3.el7.x86_64
sudo yum install -y epel-release
sudo yum install -y net-tools
sudo yum install -y python34
sudo yum install -y python34-pip


##Install python docker library
sudo pip3.4 install docker
sudo pip3.4 install jinja2
sudo pip3.4 install phoenixdb

##Start Docker deamon##
sudo systemctl start docker
sudo systemctl enable docker
sleep 5

##Make Directories
mkdir ~/se_bind_mounts
mkdir ~/se_log_dir

##Verification
echo "RUN VERIFICATIONS"

echo -e "\\n4)Check if Docker deamon is installed & running"
echo -e "=============="
echo -e "\\n`docker version`"
echo -e "=============="



