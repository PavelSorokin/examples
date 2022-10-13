import sys
import requests
import subprocess
from datetime import datetime, timedelta
var = sys.argv[1::]

pg_probackup = var[0]
host = var[1:4]
instance = var[4]
port = var[5]
mode = var[6]
thread = var[7]



def backup_start():
    for i in host:
        r = requests.get('http://' + i + ':8008/master')
        if r.status_code == 200:
            set_config = subprocess.run([pg_probackup,'set-config','-B','/var/lib/pg_probackup','--instance',instance,'--remote-host',i,'--remote-user','postgres','--pgport',port,'--pguser','pgbackup','--pgdatabase','postgres','--pghost',i])
            backup = subprocess.run([pg_probackup,'backup','-B','/var/lib/pg_probackup','--instance',instance,'-b',mode,'-j',thread,'-U','pgbackup'])
            print(datetime.now(),': Backup Done')
            
def main():
    print(datetime.now(),': Starting backup',instance,'',var[6],'mode')
    backup_start()    


if __name__ == '__main__':
    main() 