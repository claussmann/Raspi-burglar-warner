install_dir = "/etc/burglar_warner"

install: service_install notifier_install
	echo -e "\e[92mInstalled!\e[0m"

motion_install:
	apt-get update
	apt-get install motion
	echo -e "\e[92mInstalled motion\e[0m"

config: directories motion_config
	bash install_scripts/config.sh
	chown -R motion:motion $(install_dir)
	echo -e "\e[92mConfiguration complete\e[0m"

service_install: config sudoers_entry motion_install
	cp Remote-Service/telegram-remote.service /etc/systemd/system/telegram-remote.service
	systemctl enable telegram-remote.service
	cp Remote-Service/telegram-remote.sh $(install_dir)/remote/telegram-remote.sh
	cp Remote-Service/service.py $(install_dir)/remote/service.py
	chmod +x $(install_dir)/remote/telegram-remote.sh
	echo -e "\e[92mInstalled remote service\e[0m"

notifier_install: config motion_install
	cp Notifier/onMotionDetected.sh $(install_dir)/notifier/onMotionDetected.sh
	cp Notifier/onPicSave.sh $(install_dir)/notifier/onPicSave.sh
	cp Notifier/onMotion.py $(install_dir)/notifier/onMotion.py
	cp Notifier/onPicSave.py $(install_dir)/notifier/onPicSave.py
	chmod +x $(install_dir)/notifier/onPicSave.sh
	chmod +x $(install_dir)/notifier/onMotionDetected.sh
	echo -e "\e[92mInstalled notifier service\e[0m"

sudoers_entry:
	bash install_scripts/sudoers_config.sh

camera_install:
	bash install_scripts/camera.sh

directories: motion_install
	mkdir -p $(install_dir)
	mkdir -p "$(install_dir)/notifier"
	mkdir -p "$(install_dir)/remote"
	mkdir -p "$(install_dir)/motion/pics"
	mkdir -p "$(install_dir)/motion/video"
	echo -e "\e[92mCreated Directories\e[0m"

motion_config: motion_install camera_install
	bash install_scripts/motion_config.sh
