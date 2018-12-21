#!/bin/bash
echo "The service will need to run some commands like poweroff without password."
read -p "Do you wish the installer to create a sudoers entry for the service?(y/N)" a
	if [ "$a" = "y" ]
	then
		echo -e "\e[93mEditing sudoers file for motion\e[0m"
		echo "#Added by Raspi-burglar-warner" >> /etc/sudoers
		echo "#Motion may shutdown the PC:" >> /etc/sudoers
		echo "motion ALL=NOPASSWD:/sbin/reboot" >> /etc/sudoers
		echo "motion ALL=NOPASSWD:/sbin/poweroff" >> /etc/sudoers
	fi
