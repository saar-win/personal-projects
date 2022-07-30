from asyncio import subprocess
import os
import subprocess
from datetime import datetime
import sys

def main():
    '''
    '''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    subprocess.run(f'echo "::set-output name=time::{current_time}"', shell=True)
    subprocess.run(f'ls -l', shell=True)
    _file = sys.argv[1]
    with open(_file, 'r') as f:
        print(f.read())

if __name__ == '__main__':
    main()