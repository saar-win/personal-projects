### This python script creates a VM for the development team


- a helper Makefile for easy control.
- All processes will create automatically when the VM will go up by the startup script:
    - Create firewall
    - Create a persistent disk for postgress app
    - Run a docker file with nginx ,postgress, flask-hello-world

# To run the VM using:
```
make create_vm
```
# To delete the VM using:
```
make delete_vm
```
# To delete in addition the persistent disk (for postgress), using:
```
make delete_vm_disk
```