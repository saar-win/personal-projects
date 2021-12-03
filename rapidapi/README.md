# This script creates a local VM server by Vagrant.

- The script can be run in two ways:
    - Create a VM by Vagrant with Ansible.
    - Create a VM by Vagrant with Terraform.

# Requirements:
### macOS:
```
brew install vagrant
brew install virtualbox \
    https://www.virtualbox.org/wiki/Downloads
```
### Linux (ubuntu 18.04)
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vagrant

sudo apt install virtualbox
```
# Using Ansible:
### Create the VM and install Nginx by following commands:
```
cd ansible && vagrant up
```
# Using Terraform:
### Create the VM and install Nginx by following commands:
```
cd terraform && vagrant up
```
