# qemu_vm_control_lib
Simple wrapper around libvirt to setup KVM VMs with networking using openvswitch

Required libraries  (Ubuntu)
apt install qemu-kvm libvirt-dev 
pip3 install libvirt-python pexpect


Prequisites
Qemnu KVM installed
Open vswitch installed 

test_kvm uses the qemu_host create multiple VM hosts named agent1 and agent2 connected together by an OpenVSwitch

After setup to Configure ip address use the virsh interface 


