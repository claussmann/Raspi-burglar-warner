#!/bin/bash
echo -e "\e[1;92mNow we will configure your telegram bot.\e[0m"
echo "The bot's token for the http api is given to you by the botfather."
echo "The token looks like this: 12345:ABCDE_FG_HI"
read -p "Enter your bot's Token:" token

echo "$token" > /etc/burglar_warner/notifier/botToken
echo "$token" > /etc/burglar_warner/remote/botToken


touch /etc/burglar_warner/notifier/chatIDs


echo "Now enter telegram-usernames that should be authorized to control the burglar-warner via telegram"
read -p "Enter a username:" username
while [ "$username" != '' ] 
do
	echo "$username" >> /etc/burglar_warner/remote/authorized
	read -p "Enter next username (empty to finish):" username
done



echo "0" > /etc/burglar_warner/remote/lastmsgID
echo "0" > /etc/burglar_warner/remote/offset
