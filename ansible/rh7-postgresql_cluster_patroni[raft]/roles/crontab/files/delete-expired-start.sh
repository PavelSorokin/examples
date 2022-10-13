#!/bin/bash
if [  -f /tmp/backup.lock ]; then
        echo "Script is working already"
        pidlock=`cat /tmp/backup.lock`
        ps -ef | grep $pidlock
        exit 1
fi
/home/postgres/scripts/delete-expired.sh $1 >> /home/postgres/log/$(date +%Y%m%d).log 2>&1
