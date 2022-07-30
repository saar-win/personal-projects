from asyncio import subprocess
import os
import subprocess
from datetime import datetime
import sys

def main():
    '''
    '''
    print(os.environ)
    obj = {
        "key_1": sys.argv[1]
    }
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    subprocess.run(f'echo "::set-output name=time::{current_time}"', shell=True)
    print(obj)

if __name__ == '__main__':
    main()