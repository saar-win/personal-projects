import yaml
import sys
import os

def main():
    '''
    '''
    _file = os.getenv('INPUT_FILE')
    yaml_file = yaml.safe_load(open(_file))
    print(yaml_file)


if __name__ == '__main__':
    main()