#!/bin/bash
DB="select datname from pg_stat_database where datname not in ('postgres','template1','template0','mamonsu')"
PSQL="/usr/pgsql-11/bin/psql"
DBNAME=$($PSQL -h localhost -A -t --field-separator ' ' --quiet -U postgres -c "$DB")
        read -ra mydb <<< $DBNAME
        for i in "${mydb[@]}";do
        ECHO=`$PSQL -h localhost -U postgres -b $i -c "vacuum analyze;"`
        if [ $ECHO = VACUUM ]; then
            curl -X POST -H 'Content-Type: application/json' --data '{"alias":"Postgres", "avatar":"https://wiki.postgresql.org/images/3/30/PostgreSQL_logo.3colors.120x120.png", "text":"'$ECHO' DONE '$i'"}' https://srv-rocket.isb/hooks/sgN9EBeBhD22HFCwr/qwMWZJG6GEckwTFwwMyh6Sjim7HaaT99FKvFoFZLKJqRqFwd -k
        else
            curl -X POST -H 'Content-Type: application/json' --data '{"alias":"Postgres", "avatar":"https://wiki.postgresql.org/images/3/30/PostgreSQL_logo.3colors.120x120.png", "text":"VACUUM ERROR '$i'"}' https://srv-rocket.isb/hooks/sgN9EBeBhD22HFCwr/qwMWZJG6GEckwTFwwMyh6Sjim7HaaT99FKvFoFZLKJqRqFwd -k
        fi
        done