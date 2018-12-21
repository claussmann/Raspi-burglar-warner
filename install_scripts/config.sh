#!/bin/bash
echo -e "\e[93mNow we will configure your telegram bot.\e[0m"
echo "The bot's token for the http api is given to you by the botfather."
echo "The token looks like this: 12345:ABCDE_FG_HI"
read -p "Enter your bot's Token:" token

echo "$token" > /etc/burglar_warner/notifier/botToken
echo "$token" > /etc/burglar_warner/remote/botToken


echo "Now: The notifier.\nIt will always notify you if motion is detected."
echo "You can now enter all chatIDs that you want to be notified at motion detection"
read -p "Enter a chatID:" chatID
while [ "$chatID" != '' ] 
do
	echo "$chatID" >> /etc/burglar_warner/notifier/chatIDs
	read -p "Enter next chatID (empty to finish):" chatID
done


echo "Finally: The remote-controller!"
echo "Now enter telegram-usernames that should be authorized to control the burglar-warner via telegram"
read -p "Enter a username:" username
while [ "$username" != '' ] 
do
	echo "$username" >> /etc/burglar_warner/remote/authorized
	read -p "Enter next username (empty to finish):" username
done



echo "0" > /etc/burglar_warner/remote/lastmsgID
echo "0" > /etc/burglar_warner/remote/offset
