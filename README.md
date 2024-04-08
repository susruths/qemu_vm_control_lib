# qemu_vm_control_lib
This is a simple python based wrapper around libvirt to programmatically put together a system using KVM VMs and openvswitch for networking.

# Required libraries  (Ubuntu)
- apt install qemu-kvm libvirt-dev 
- pip3 install libvirt-python pexpect


# Prequisites
- Qemnu KVM installed
- Open vswitch installed 

# Usage
The usage is very straighforward. First the parameters of the system needs to be defined in JSON format as below. 

```javascript
{
  vm1_params = {"name":"agent1", "ip":"10.1.1.1/24", "mac":"52:54:00:bc:03:02", "source_bridge":"ovsbr0", "memory":"2097152", "vcpu":"2", "image":'cosim-vm01.qcow2', "userid":"intel", "pwd":"intel123"}
}
```

test_kvm.py uses the qemu_host create multiple VM hosts named agent1 and agent2 connected together by an OpenVSwitch
The VM properties are defined as a dictionary in test_kvm.py as follows


vm2_params = {"name":"agent2", "ip":"10.1.1.2/24", "mac":"52:54:00:bc:03:03", "source_bridge":"ovsbr0", "memory":"2097152", "vcpu":"2", "image":'cosim-vm02.qcow2', "userid":"intel", "pwd":"intel123"}

The "image" specifed has to be present in teh directory 
/opt/cosim/vm_images/

The user name and password also needs to be set appropriately according to the image.

After setup to Configure ip address use the virsh interface. 


