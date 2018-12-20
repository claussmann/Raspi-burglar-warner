install_dir = "/burglar_warner"

install: service_install notifier_install

motion_install:
	apt-get update
	apt-get install motion

config:

service_install: config sudoers_entry

notifier_install: config motion_install

sudoers_entry:
	bash install_scripts/sudoers_config.sh

camera_install:

directories:
	mkdir -p $(install_dir)
	chown motion:motion $(install_dir)
