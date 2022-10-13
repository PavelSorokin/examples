#!/bin/bash
instance=$1
pg_probackup=$2
if [ "$($pg_probackup show --instance=$instance -B /pg_backup --format=json | jq -c '.[].backups[0].status')" == '"OK"' ];
        then   result=0;
        else   result=1;
fi
/bin/zabbix_sender -c /etc/zabbix/zabbix_agent2.conf -k pgsql.db.backup -o $result