from asyncio import subprocess
import os
import subprocess
from datetime import datetime
import sys

def main():
    '''
    '''
    obj = {
        "key_1": sys.argv[1],
        "key_2": sys.argv[2],
        "key_3": sys.argv[3],
        "key_4": sys.argv[4]
    }
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    subprocess.run(f'echo "::set-output name=time::{current_time}"', shell=True)
    return obj

if __name__ == '__main__':
    main()