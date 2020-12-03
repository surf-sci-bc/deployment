# Configuration

Put the config file into the right directory (assumes you are in this repo's root):

```sh
$ sudo cp tljh/jupyterhub_config.py /opt/tljh/config/jupyterhub_config.d
$ sudo tljh-config reload
```

# Mounting the surfer data file

Open fstab by `sudo nano /etc/fstab`. Then add this line:

```
# Add to /etc/fstab
//192.168.2.99/data   /home/agfalta/data    cifs    credentials=/home/agfalta/.credentials,auto,ro,mfsymlinks   0   0
```

You need to have the credentials of the data servers samba user in the above mentioned file in this form:
```
# /home/agfalta/.credentials
user=xxx
password=xxx
```

Also install cifs and finally mount the data volume:

```sh
$ sudo apt install cifs-utils
$ sudo mount -a
```
