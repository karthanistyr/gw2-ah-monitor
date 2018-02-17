#!/bin/sh

USERNAME=gw2-ah-monitor
USERGRP=gw2-ah-monitor
LOCALDIR='/var/lib/gw2-ah-monitor'

id -u $USERNAME > /dev/null
if [ $? -eq 1 ]; then
  useradd --system -M --base-dir /var/lib --shell /bin/false --user-group $USERNAME
fi

if [ ! -d "$LOCALDIR" ]; then
  mkdir $LOCALDIR
  chgrp -R $USERGRP $LOCALDIR
  chown -R $USERNAME $LOCALDIR
fi

python `dirname $0`/gw2-ah-monitor.py
