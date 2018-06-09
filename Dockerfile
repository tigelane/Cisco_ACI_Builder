FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>

RUN apt-get update
RUN apt-get -y upgrade

###########
# apt-get
###########
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-setuptools python-pip
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git vim
RUN DEBIAN_FRONTEND=noninteractive pip install --upgrade pip

###########
# ACI Toolkit Install
###########
WORKDIR /root
RUN git clone https://github.com/datacenter/acitoolkit.git
WORKDIR /root/acitoolkit
RUN python setup.py install
WORKDIR /root

###########
# Cisco ACI Scripts
###########
RUN git clone https://github.com/tigelane/cisco_aci-scripts.git
