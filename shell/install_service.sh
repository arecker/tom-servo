#!/usr/bin/env bash
# install_service.sh
# Installs the virtualbox service in the systemd root
if [ "$EUID" -ne 0 ]; then
    echo "shouldn't you be root?"
    exit 1
fi

CURDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SYSTEMD_ROOT=/etc/systemd/system
cp ${CURDIR}/../systemd/vboxvmservice@.service ${SYSTEMD_ROOT}

echo "Script installed
run the following command to start the service:
sudo systemctl start vboxvmservice@'your vm name'"
exit