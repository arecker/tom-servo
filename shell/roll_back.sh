#!/usr/bin/env bash
# roll_back.sh "machine name" "snapshot name"
# Rolls the virtualmachine to a named snapshot

/usr/bin/vboxmanage controlvm "$1" poweroff
/usr/bin/vboxmanage snapshot "$1" restore "$2"