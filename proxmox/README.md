# Setting up Proxmox for Jupyterhub Server

## Proxmox installation

### Create USB

Download the latest Proxmox .iso image from https://www.proxmox.com/de/downloads/category/iso-images-pve.

When creating USB for Proxmox on Windows via Rufus choose DD mode for writing, otherwise the USB is not identified. For other Programs such as Etcher, it seems to work out of the box. Plug in the USB drive an boot the server.  

Make sure that Virtualization is activated in BIOS.

### Install the Hypervisor

The Proxmox installer should be straight forward. Enter network settings, admin password etc. For the hard drive configuration choosing ZFS as a filesystem gives some nice features, as it supports software raid (also it demands software raid) and it supports copy-on-write which enables fast snapshot creations of the filesystem. However, ZFS is also very greedy in terms of memory, so you have to calculate a 4GB RAM + 1GB/TB of Storage.

After the installation is complete the proxmox webi nterface is reacheable at ```https://<proxmox-ip>:8006```. The ```https://``` is mandatory.

### Configuration of Hypervisor

When you enter the webminterface log in with Username: ```root``` and the password chosen during installation. Make yourself familiar with the interface.

On the left hand side you see the Datacenter. It may only have one node, which is the server you are currently working on. When you expand the node you see the storages that were configured during installation. By selecting the node you see the options of the node. Most notably you can enter the shelly of the node over the web interface to enter commands.

As we don't own a subscription for proxmox the ```/etc/apt/sources.list``` must be adapted to use the community repository instead of the enterprise repository

```
nano /etc/apt/sources.lists
```
Add to end of file:
```
# PVE pve-no-subscription repository provided by proxmox.com,
# NOT recommended for production use
deb http://download.proxmox.com/debian/pve buster pve-no-subscription
```
Finally remove enterprise file:
```
rm /etc/apt/sources.list.d/pve-enterprise.list
```
Now you can ```apt update```

Updates can also be installed by selecting the node in the GUI and selecting Updates.

## Install VMs

Now we are ready to install a VM. Select the storage ```local```, which is the storage to upload your VMs to. Select ```ISO Images``` and upload your .iso.

Now click ```Create VM``` on the top of the page. A window opens. Choose the Settings as following:
1. General: Select the node you want to install the VM (Probably this one). Choose a name for the VM (like Jupyterhub).  
2. OS: Select the ISO you want to install from storage ```local```. Choose settings of the Guest OS. Probably Linux, so standard settings are fine.  
3. System: Graphics card can stay default, unless you want to use SPICE to enter the GUI of the VM. This ist not necessary for headless VMs, but offers good performance when you want to use Ubuntu Desktop. But still don`t expect to get, bare metal performance with a GUI. Select VirtIO SCSI and tick Qemu Guest Agent.  
4. Hard Disk: Choose the storage location for the VMs disk and the disksize to your pleasure. For cache you can use different options: Choose ```None``` or ```writethrough```, where ```None```is better for writing heavy applications and ```writethrough``` for reading heavy applications. ```writeback```is faster but may loose data on power outage, unless you gave a capacitor backed SSD, which you probably don`t.
5. CPU: Choose Sockets depending on the number of Sockets of your Server (probably 1). Choose as many Cores as you like but not more than your CPU has. When you have multiple VMs on one server it is fine to overcommitted your cores by a factor of 4, as most of your VMs will idle most of the time.   
For type choose Host for best performance, as this will emulate the vCPUs to be of the same type as the host CPU. When you are intending to migrate the VMs between different nodes, choose the Default (kvm64). This makes no assumptions over the features of the CPU and is compatible with everything.

6. Memory: Choose memory as you like. Remember that memory cannot be overcommitted and VMs can only start if enough memory is available in RAM+SWAP at startup. By choosing Ballooning device, the VM can increase its maximum memory if memory is available but will have at least the minimum reserved memory.

7. Network: Choose VirtIO for best performance

8. Check and confirm your settings.

Under the node the VM should appear with it`s given name and VM id (e.g. Jupyterhub(100)). Start the VM. Go to ```Console``` and install the OS from the .iso. 

### Install guest agent

After installation install the ```qemu-guest-agent```, so proxmox can interface itself with the VM to establish a network connection etc.

```
sudo apt install qemu-guest-agent
```

Now it`s also possible to SSH into the VM at the IP address of the VM (stated under Summary).

If you want to use spice install also:
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
