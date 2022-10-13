import sys
import subprocess
import psycopg2
from datetime import datetime, timedelta
var = sys.argv[1::]

pg_probackup = var[0]
host = var[1:3]
instance = var[3]
port = var[4]
mode = var[5]
thread = var[6]

def backup_check_master():

    for i in host:
        try:
            conn = psycopg2.connect(host=i,
                    port=port,
                    database='postgres',
                    user='pgbackup',
                    password='7OoJXh1-HNSsD91-8WrAp')          
        except psycopg2.OperationalError as err:
            print(err)
            conn = None
        if conn != None:
            cursor = conn.cursor()
            cursor.execute('show transaction_read_only;')
            row = cursor.fetchone()
            if row == ('off',):
                host_master = i
            cursor.close()

    backup_start(host_master)

def backup_start(host_master):

    set_config = subprocess.run([pg_probackup,'set-config','-B','/var/lib/pg_probackup','--instance',instance,'--remote-host',host_master,'--remote-user','postgres','--pgport',port,'--pguser','pgbackup','--pgdatabase','postgres','--pghost',host_master])
    backup = subprocess.run([pg_probackup,'backup','-B','/var/lib/pg_probackup','--instance',instance,'-b',mode,'-j',thread,'-U','pgbackup'])
    print(datetime.now(),': Backup Done')

def main():
    print(datetime.now(),': Starting backup',instance,'',var[5],'mode')
    backup_check_master()
    
if __name__ == '__main__':
    main()