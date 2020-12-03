# Setting up Proxmox for TLJH-Server

When creating USB for Proxmox via Rufus choose DD mode for writing, otherwise the USB is not identified.  
Seems Zfs would be a good Filesystem for Proxmox as it supports copy-on-write for fast snapshot creation

remember to install guest additions on Proxmox for Ip adress etc.

```
sudo apt install qemu-guest-agent
```

If you want to use spice:
````
sudo apt install spice-vdagent
````

## Resize partition after increasing storage (just in case)
Find out which partition needs to be resized
````
$ sudo fdisk -l

/dev/sda1   1G
/dev/sda2   2G
/dev/sda3   30G <- This one

````
Resize partition to maximum:
````
$ sudo pvresize /dev/sda3
````

Find out the logical volume that resides in the partition:

````
$ df -h

dev 3.9G
mpfs  798M
/dev/mapper/ubuntu--vg-ubuntu--lv 20G <- name looks similar to this
/dev/sda2 976M
````

Resize logical volume to full partition:

````
$ sudo lvextend -r -l +100$FREE /dev/mapper/ubuntu--vg-ubuntu--lv
````
