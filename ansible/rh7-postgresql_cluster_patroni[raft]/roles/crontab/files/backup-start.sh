#!/bin/bash
if [  -f /tmp/backup.lock ]; then
        echo "Script is working already"
        pidlock=`cat /tmp/backup.lock`
        ps -ef | grep $pidlock
        exit 1
fi
echo $$ > /tmp/backup.lock
/bin/python3.6 /home/postgres/scripts/backup.py $1 $2 $3 $4 >> /home/postgres/log/$(date +%Y%m%d).log 2>&1
/bin/rm /tmp/backup.lock