from asyncio import subprocess
import os
import subprocess
from datetime import datetime

def main():
    '''
    '''
    obj = {
        "key_1": os.environ.get("key_1", "None"),
        "key_2": os.environ.get("key_2", "None"),
        "key_3": os.environ.get("key_3", "None"),
        "key_4": os.environ.get("key_4", "None")
    }
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    subprocess.run(f'echo "::set-output name=time::{current_time}"', shell=True)
    print(obj)
    return obj

if __name__ == '__main__':
    main()