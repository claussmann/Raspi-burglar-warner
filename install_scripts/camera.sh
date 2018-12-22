#!/bin/bash
read -p "Have you already configured your camera? (y/N)" a
if [ "$a" != "y" ]
then
	read -p "Do you want to configure an official Raspi-Camera? (Y/n)" b
	if [ "$b" != "n" ]
	then
		echo "Loading default cameramodule in /etc/modules"
		echo "#default Camera" >> /etc/modules;
		echo "bcm2835-v4l2" >> /etc/modules;
	else
		echo "\e[1;91mCannot configure your camera. Please load the modules on your own.\e[0m"
	fi
fi
