import sys
import socket
import subprocess
from datetime import datetime, timedelta
var = sys.argv[1::]

print(datetime.now(),': Starting backup ',var[2],' mode')
read_only = subprocess.run(['psql','-U','postgres','-Atc','show transaction_read_only'], universal_newlines = True, stdout = subprocess.PIPE)
read_only_lines = read_only.stdout.splitlines()
for i in read_only_lines:
        if i  == 'off':
                result = subprocess.run(['pg_probackup-13','backup','-B',var[0],'--instance',var[1],'-b',var[2],'-j',var[3],'-U','backup'])
                print(datetime.now(),': Backup Done')
                subprocess.run(['/home/postgres/scripts/zbx_backup_check.sh',var[1],'pg_probackup-13'])               
        else:
                print(datetime.now(),': Backup not runing, no master node')