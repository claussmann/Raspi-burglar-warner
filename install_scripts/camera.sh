read -p "Have you already installed your camera? (y/N)" b
if [ "$b" != "y" ] 
then
	echo "Loading default cameramodule in /etc/modules"
	echo "#default Camera" >> /etc/modules;
	echo "bcm2835-v4l2" >> /etc/modules;
fi
