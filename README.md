### ESXi fabfile

Simple Fabric fabfile to clone a VM from a template on VMware ESXi

***Instal fabric***
```
#> pip install fabric
```
More informations on Fabric installation : http://www.fabfile.org/installing.html

**Usage :**
```
fab -list
Available commands:

    esx.clone_vm  Read configuration from json file and clone VM
```

```
fab -H root@<your_esxi_host> esx.clone_vm:myvm-settings.json
```

```
[root@esxi] Executing task 'esx.clone_vm'
>>> Creating VM: myvm-dev
Creating target VM myvm-dev folder /vmfs/volumes/datastore1/myvm-dev
[root@esxi] run: mkdir /vmfs/volumes/datastore1/myvm-dev
Cloning disk /vmfs/volumes/datastore1/ubuntu-1404-64bit/ubuntu-1404-64bit.vmdk
Cloning. done!
[root@esxi] put: <file obj> -> /vmfs/volumes/datastore1/myvm-dev/myvm-dev.vmx
[root@esxi] run: vim-cmd solo/registervm /vmfs/volumes/datastore1/myvm-dev/myvm-dev.vmx
[root@esxi] out: 44
[root@esxi] out: 
...
```

**Sample configuration file :**
```json
{
  "datastore": "/vmfs/volumes/datastore1",

  "template": [
    {
      "name": "ubuntu-1404-64bit",
      "vmdk" : "/vmfs/volumes/datastore1/ubuntu-1404-64bit/ubuntu-1404-64bit.vmdk",
      "vmx_file": "ubuntu-1404-64bit.vmx"
    }
  ],
  "VM": [
    {
      "name": "myvm-dev",
      "memory": "2048",
      "guestos":"ubuntu-64",
      "numcpus": 2,
      "coresPerSocket": 2,
      "disk_provisioning": "thin"
    }
  ]
}

```

- Fabric: http://www.fabfile.org
