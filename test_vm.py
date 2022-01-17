from qemu_host import QemuHost
import subprocess
import time
import pdb



vm1_params = {"name":"agent1", "ip":"10.1.1.1/24", "mac":"52:54:00:bc:03:02", "source_bridge":"ovsbr0", "memory":"2097152", "vcpu":"2", "image":'cosim-vm01.qcow2', "userid":"intel", "pwd":"intel123"}
vm2_params = {"name":"agent2", "ip":"10.1.1.2/24", "mac":"52:54:00:bc:03:03", "source_bridge":"ovsbr0", "memory":"2097152", "vcpu":"2", "image":'cosim-vm02.qcow2', "userid":"intel", "pwd":"intel123"}

# create the bridge before creating host
def ovs_del( name ):
    # Check to make sure that the source bridge exists
    bridges = subprocess.check_output("ovs-vsctl show", stderr=subprocess.STDOUT, shell=True)
    if 'Bridge %s'%name in str(bridges):
        out = subprocess.check_output("ovs-vsctl del-br %s"%name, stderr=subprocess.STDOUT, shell=True)


def ovs_create( name, remove_existing=True ):
    # Check to make sure that the source bridge exists
    bridges = subprocess.check_output("ovs-vsctl show", stderr=subprocess.STDOUT, shell=True)
    if 'Bridge %s'%name in str(bridges) and remove_existing:
        out = subprocess.check_output("ovs-vsctl del-br %s"%name, stderr=subprocess.STDOUT, shell=True)

    bridges = subprocess.check_output("ovs-vsctl add-br %s"%name, stderr=subprocess.STDOUT, shell=True)



ovs_create("ovsbr0")
host1 = QemuHost.create(vm1_params) 
host2 = QemuHost.create(vm2_params) 

print ('Instance is created ....')

while True:
    text = input("Enter to start simulation: ")
    if text == "exit":
        break

    #host.pause()

    #sleep(10)

    #host.resume()

for host in [host1, host2]:
    if host is not None:
        host.stop()

ovs_del( "ovsbr0" )
