from asyncio import subprocess
import os
import subprocess
from datetime import datetime
import sys

def main():
    '''
    '''
    print(os.environ)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    subprocess.run(f'echo "::set-output name=time::{current_time}"', shell=True)

    var = sys.argv[1]
    print(var)

if __name__ == '__main__':
    main()