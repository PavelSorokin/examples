SELECT pid,(now() - pg_stat_activity.xact_start) AS age, datname, usename, client_addr, wait_event_type, wait_event, state,query  FROM pg_stat_activity 
WHERE ((pg_stat_activity.xact_start IS NOT NULL) 
AND ((now() - pg_stat_activity.xact_start) > '00:00:00.5'::interval)) 
ORDER BY pg_stat_activity.xact_start;




SELECT
    pid,
    pg_catalog.pg_blocking_pids(pid) AS blocking_pids,
    datname,
    usename,
    pg_catalog.to_char(backend_start, 'YYYY-MM-DD HH24:MI:SS TZ') AS backend_start,
    state,
    wait_event_type || ': ' || wait_event AS wait_event,
    pg_catalog.pg_blocking_pids(pid) AS blocking_pids,
    pg_catalog.to_char(state_change, 'YYYY-MM-DD HH24:MI:SS TZ') AS state_change,
    pg_catalog.to_char(query_start, 'YYYY-MM-DD HH24:MI:SS TZ') AS query_start,
    backend_type,
    query
FROM
    pg_catalog.pg_stat_activity
ORDER BY pid