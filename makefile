install: service_install notifier_install

run: install

run_on_startup: install

motion_install:
	apt-get update
	apt-get install motion

config:

service_install: config

notifier_install: config motion_install
