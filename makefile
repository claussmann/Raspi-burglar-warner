install_dir = "/etc/burglar_warner"

install: service_install notifier_install

motion_install:
	apt-get update
	apt-get install motion

config:

service_install: config sudoers_entry
	cp Remote-Service/telegram-remote.service /etc/systemd/system/telegram-remote.service
	systemctl enable telegram-remote.service

notifier_install: config motion_install

sudoers_entry:
	bash install_scripts/sudoers_config.sh

camera_install:

directories:
	mkdir -p $(install_dir)
	mkdir -p "$(install_dir)/notifier"
	mkdir -p "$(install_dir)/remote"
	chown -R motion:motion $(install_dir)
