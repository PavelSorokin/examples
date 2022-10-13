# PostgreSQL High-Availability Cluster with Raft protocol
---

Плейбук для построения отказоустойчивого кластера Postgresql на базе patroni[raft]

Доступные архитектуры (настраивается в inventory ):

    1. 2 сервера db + quorum
    
    2. 3 сервера db 

## Compatibility
RedHat based distros (x86_64)

###### Supported Linux Distributions:
- **CentOS**: 7
- **RedHat**: 7
###### PostgreSQL versions:
:white_check_mark: tested, works fine: `PostgreSQL 13`
###### Ansible version 
This has been tested on Ansible 2.7, 2.8, 2.9, 2.10, 2.11

###### Запуск Playbook
1. Перейти в директорию

`cd patroni/`

2. Внести изменения в inventory

###### Specify the ip addresses and connection settings (`ansible_user`, `ansible_ssh_pass` ...) for your environment

`vim inventory`

4. Иправить переменные:

    1./[main.yml](./vars/main.yml) - Основные переменные для PostgreSQL и Patroni 

    2./[install_roles.yml](./vars/install_roles.yml) - True or Fasle, Можно задать какие роли пропустить 

`vim vars/main.yml` 

Please change:

`cluster_vip: "Твой IP для keepalived"`

`pg_probackup_instance`

`pg_probackup_thread`

`shared_buffers`

`work_mem`

`maintenance_work_mem`

`effective_cache_size`

`max_worker_processes`

`max_parallel_workers`

`max_parallel_workers_per_gather`

`max_parallel_maintenance_workers`

`pgsqlrep_password`

`postgres_password`

`vim vars/install_roles.yml`


5. Run playbook:

`ansible-playbook deploy-postgres.yml -u p.sorokin`

`ansible-playbook pg_extensions.yml -u p.sorokin`