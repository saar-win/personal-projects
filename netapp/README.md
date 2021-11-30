### This python script creates a VM for the development team


- A helper Makefile for easy control.
- All processes will create automatically when the VM goes up by the startup script:
    - Create a firewall.
    - Create a persistent disk for the postgress app.
    - Run a docker file with nginx ,postgress, flask-hello-world.
    - There is a variable yaml that describes all the information that needs be.
# To create the VM using:
```
make create_vm
```
# To delete the VM using:
```
make delete_vm
```
# To delete in addition the persistent postgress disk using:
```
make delete_vm_disk
```