import yaml
import os

def main():
    '''
    '''
    file_path = os.getenv('INPUT_FILE')
    yaml_file = yaml.safe_load(open(file_path))
    print(yaml_file)


if __name__ == '__main__':
    main()