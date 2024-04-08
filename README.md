# qemu_vm_control_lib
This is a simple python based wrapper around libvirt to programmatically put together a system using KVM VMs and openvswitch for networking.

# Required libraries  (Ubuntu)
- apt install qemu-kvm libvirt-dev 
- pip3 install libvirt-python pexpect


# Prequisites
- Qemu KVM installed
- Open vswitch installed 

# Usage
The usage is very straighforward. First the parameters of the system needs to be defined in JSON format as below. 

```javascript
{
  vm1_params = {
        "name":"agent1",
        "ip":"10.1.1.1/24",
        "mac":"52:54:00:bc:03:02",
        "source_bridge":"ovsbr0",
        "memory":"2097152",
        "vcpu":"2",
        "image":'cosim-vm01.qcow2',
        "userid":"intel",
        "pwd":"intel123"}
}

vm2_params = {
        "name":"agent2",
        "ip":"10.1.1.2/24",
        "mac":"52:54:00:bc:03:03",
        "source_bridge":"ovsbr0",
        "memory":"2097152",
        "vcpu":"2",
        "image":'cosim-vm02.qcow2',
        "userid":"intel",
        "pwd":"intel123"
}
```

import QemuHost from qumu_host.py
Use the static class method in QemuHost to create a VM host. 
```
QemuHost.create()
```

The architecture template of the virtual machine created can changed through the
QemuHost.domain_config_template variable. This template defines the configuration of the 
virtual machine in terms of memory, cpu, power management, and devices like networking
disk, controllers etc. 

Once a VM is created, the instance can be managed using the following API exposed by the
QemuHost object

start()
Stop()
pause()

test_kvm.py is a sample usege script theat uses the qemu_host to create multiple VM hosts named agent1 and agent2 connected together by an OpenVSwitch
The VM properties are defined as a dictionary in test_kvm.py as follows


The "image" specifed has to be present in teh directory 
/opt/cosim/vm_images/

The user name and password also needs to be set appropriately according to the image.

After setup to Configure ip address use the virsh interface. 


