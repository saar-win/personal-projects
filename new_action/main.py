import yaml
import sys

def main():
    '''
    '''
    _file = sys.argv[1]
    yaml_file = yaml.safe_load(open(_file))
    print(yaml_file)


if __name__ == '__main__':
    main()