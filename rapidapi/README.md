### This script creates a local vm server by Vagrant

- There is a 2 scripts method:
    - Create a VM by Vagrant with Ansible.
    - Create a VM by Vagrant with Terraform.

# Requierments:
### macOS:
```
brew install vagrant
brew install virtualbox \
    https://www.virtualbox.org/wiki/Downloads
```
# To create the vm and install the nginx web server by ansible, using:
```
cd ansible && vagrant up
```
# To create the vm and install the nginx web server by terraform, using:
```
cd terraform && vagrant up
```