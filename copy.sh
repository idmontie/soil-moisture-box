#!/bin/bash

# Copy this folder to a pi via SSH

rsync -avz "$(pwd)" pi@raspberrypi.local:~/