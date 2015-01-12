# -*- coding: utf-8 -*-

import json
from utils.progressbar import progress_bar_loading

from fabric.api import *
from fabric.colors import green
from fabric.contrib import files
from fabric.contrib.files import exists


# ESXi doesn't include bash
env.shell = "/bin/sh -c"


def clone_vmdk(source_vmdk, dest_vmdk, disk_provisioning):
    """
    VMDK Clone
    """
    print(green("Cloning disk %s" % source_vmdk))

    kill = False
    stop = False
    p = progress_bar_loading(stop, kill, 'Cloning...')
    p.start()

    try:
        with hide('output','running','warnings'), settings(warn_only=True):
            status  = run("""vmkfstools -i "%s" "%s" -d %s""" % (source_vmdk, dest_vmdk, disk_provisioning)).succeeded
        p.stop = True
    except KeyboardInterrupt or EOFError:
        p.kill = True
        p.stop = True

    return status


def vm_exist(vmname):
    """
    Check if VM is registered
    """
    with hide('output','running','warnings'), settings(warn_only=True):
        result = run("""vim-cmd vmsvc/getallvms | sed -e '1d' -e 's/ \[.*\]//' | awk '{print $1 ":" $2 ":" $3}' | grep ':%s:'""" % vmname)

    return result.split(":") if result.return_code == 0 else None


def vm_is_powered(vmid):
    """
    Check if VM is powered
    """
    with hide('output','running','warnings'), settings(warn_only=True):
        result = run("""vim-cmd vmsvc/power.getstate %s | tail -1""" % vmid)

    return True if result == "Powered on" else None

def folder_exist(path):
    return True if exists(path) else None


def register_vm(vmx_path):
    """
    Register VM
    """
    run("""vim-cmd solo/registervm %s""" % vmx_path) if exists(vmx_path) else None

def upload_vmx(vm, vm_path):
    """
    Upload vm.vmx file
    """
    env.vm = vm

    source_file = 'myvmx.jinja.vmx'
    template_dir = 'template'
    destination_file = vm_path + "/" + vm["name"] + ".vmx"
    template = files.upload_template(source_file, destination_file, use_jinja=True, template_dir=template_dir, context=env, mode=0644)

    return template[0] if template.succeeded else None

def get_vmx_info(vmname):
    """
    Use vim-cmd to guess vmx file (basedir datastore_path)
    cmd: vim-cmd vmsvc/getallvms | sed -e '1d' -e 's/ \[.*\]//' | awk '{print $1 ":" $2 ":"  $3}' | grep template_name
    """
    pass


def apply_config():
    """
    Apply additional configuration (Hostname, LAMP, Mail ...)
    """
    pass

@task
def clone_vm(config_file):
    """
    Read configuration from json file and clone VM
    """

    #Read JSON file
    data = json.loads(open(config_file).read())

    #Check if template exists and is powered off
    template_id = vm_exist(data["template"][0]["name"])
    if template_id:
        if vm_is_powered(template_id[0]):
            raise SystemExit("ERROR - Template VM %s is powered on." % data["template"][0]["name"])
    else:
        raise SystemExit("ERROR - Template VM %s not found." % data["template"][0]["name"])

    for vm in data["VM"]:
        # Check if VMs exists
        if vm_exist(vm["name"]):
            raise SystemExit("ERROR - VM %s already exist." % vm["name"])
        else:
            print(green(">>> Creating VM: %s" % vm["name"]))

            vm_path = data["datastore"] + "/" + vm["name"]
            if folder_exist(vm_path):
                raise SystemExit("ERROR - Target VM %s directory already exist" % vm_path)
            else:
                print("Creating target VM %s folder %s" % (vm["name"], vm_path))
                run("""mkdir %s""" % vm_path)

                clone_vmdk(data["template"][0]["vmdk"], vm_path + "/" + vm["name"] + ".vmdk", vm["disk_provisioning"])

                vm["numvcpus"] = vm['numcpus'] * vm['coresPerSocket']
                vmx_path = upload_vmx(vm, vm_path)
                register_vm(vmx_path)
