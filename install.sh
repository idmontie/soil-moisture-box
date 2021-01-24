#!/bin/bash

# Set up environment

cd "$(dirname "$0")"

if ! command -v node &> /dev/null
then
    sudo apt-get update
    sudo apt-get dist-upgrade
    curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
    sudo apt-get install -y nodejs npm
fi

pip3 install -r ./requirements.txt
