import libvirt
import pexpect, sys
import pprint
import logging
import subprocess
import pdb
import time, os
from qemu_console import QemuConsole


'''
    QemuHost
        A simple  wrapper around libvirt for creating KVM -VM' using a specific domain template 
        The domain template can be customized using certain parameters. 
'''

class QemuHost:

    domain_config_template= """
      <domain type='kvm' id='$DOMAIN_ID'>
        <name>$DOMAIN_NAME</name>
        <memory unit='KiB'>$MEMORY</memory>
      <currentMemory unit='KiB'>$MEMORY</currentMemory>
      <vcpu placement='static'>$VCPUS</vcpu>
      <os>
        <type arch='x86_64' machine='pc-q35-4.2'>hvm</type>
        <boot dev='hd'/>
      </os>
      <features>
        <acpi/>
        <apic/>
        <vmport state='off'/>
      </features>
      <cpu mode='host-model' check='partial'/>
      <clock offset='utc'>
        <timer name='rtc' tickpolicy='catchup'/>
        <timer name='pit' tickpolicy='delay'/>
        <timer name='hpet' present='no'/>
      </clock>
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>destroy</on_crash>
      <pm>
        <suspend-to-mem enabled='no'/>
        <suspend-to-disk enabled='no'/>
      </pm>
      <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='/opt/cosim/vm_images/$DOMAIN_IMG'/>
          <target dev='vda' bus='virtio'/>
          <address type='pci' domain='0x0000' bus='0x03' slot='0x00' function='0x0'/>
        </disk>
        <disk type='file' device='cdrom'>
          <driver name='qemu' type='raw'/>
          <target dev='sda' bus='sata'/>
          <readonly/>
          <address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
        <controller type='usb' index='0' model='ich9-ehci1'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x7'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci1'>
          <master startport='0'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x0' multifunction='on'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci2'>
          <master startport='2'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x1'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci3'>
          <master startport='4'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x1d' function='0x2'/>
        </controller>
        <controller type='sata' index='0'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x1f' function='0x2'/>
        </controller>
        <controller type='pci' index='0' model='pcie-root'/>
        <controller type='pci' index='1' model='pcie-root-port'>
          <model name='pcie-root-port'/>
          <target chassis='1' port='0x10'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0' multifunction='on'/>
        </controller>
        <controller type='pci' index='2' model='pcie-root-port'>
          <model name='pcie-root-port'/>
          <target chassis='2' port='0x11'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x1'/>
        </controller>
        <controller type='pci' index='3' model='pcie-root-port'>
          <model name='pcie-root-port'/>
          <target chassis='3' port='0x12'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x2'/>
        </controller>
        <controller type='pci' index='4' model='pcie-root-port'>
          <model name='pcie-root-port'/>
          <target chassis='4' port='0x13'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x3'/>
        </controller>
        <controller type='pci' index='5' model='pcie-root-port'>
          <model name='pcie-root-port'/>
          <target chassis='5' port='0x14'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x4'/>
        </controller>
        <controller type='pci' index='6' model='pcie-root-port'>
          <model name='pcie-root-port'/>
          <target chassis='6' port='0x15'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x5'/>
        </controller>
        <controller type='virtio-serial' index='0'>
          <address type='pci' domain='0x0000' bus='0x02' slot='0x00' function='0x0'/>
        </controller>
        <interface type='bridge'>
            <mac address='$MAC_ADDR'/>
            <source bridge='$SRC_BRIDGE'/>
            <virtualport type='openvswitch'/>
            <target dev='vnet1'/>
            <model type='e1000'/>
            <alias name='net1'/>
            <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
        </interface>
        <serial type='pty'>
          <target type='isa-serial' port='0'>
            <model name='isa-serial'/>
          </target>
        </serial>
        <console type='pty'>
          <target type='serial' port='0'/>
        </console>
        <channel type='unix'>
          <target type='virtio' name='org.qemu.guest_agent.0'/>
          <address type='virtio-serial' controller='0' bus='0' port='1'/>
        </channel>
        <channel type='spicevmc'>
          <target type='virtio' name='com.redhat.spice.0'/>
          <address type='virtio-serial' controller='0' bus='0' port='2'/>
        </channel>
        <input type='tablet' bus='usb'>
          <address type='usb' bus='0' port='1'/>
        </input>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <graphics type='spice' autoport='yes'>
          <listen type='address'/>
          <image compression='off'/>
        </graphics>
        <sound model='ich9'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x1b' function='0x0'/>
        </sound>
        <video>
          <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1' primary='yes'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
        </video>
        <redirdev bus='usb' type='spicevmc'>
          <address type='usb' bus='0' port='2'/>
        </redirdev>
        <redirdev bus='usb' type='spicevmc'>
          <address type='usb' bus='0' port='3'/>
        </redirdev>
        <memballoon model='virtio'>
          <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
        </memballoon>
        <rng model='virtio'>
          <backend model='random'>/dev/urandom</backend>
          <address type='pci' domain='0x0000' bus='0x05' slot='0x00' function='0x0'/>
        </rng>
      </devices>
    </domain>
    """
    '''
      For adding Shared Memory
      domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
      <qemu:commandline>
          <qemu:arg value='-chardev'/>
          <qemu:arg value='socket,path=/tmp/ivshmem_socket,id=ivshmem_socket'/>
          <qemu:arg value='-device'/>
          <qemu:arg value='ivshmem,chardev=ivshmem_socket,size=1m'/>
      </qemu:commandline>

      or 

      <filesystem type='mount' accessmode='passthrough'>
        <source dir='host_dir_path'/>
        <target dir='testlabel'/>
      </filesystem>

    '''
    def __init__( self, name, console, conn, dom, userid, pwd, ip, mac ):
        self.name = name
        self.ip = ip
        self.userid = userid
        self.pwd = pwd
        self.mac = mac
        self.conn = conn
        self.dom = dom
        self.console = console
        self.configure()

    def configure(self):
      # set ip
      cmd = "sudo -s --  'ip addr add %s dev enp1s0;sleep 1;ip link set up dev enp1s0'" % self.ip
      # TODO set teh hostname
      # cmd = sudo hostnamectl set-hostname self.name
      self.cmd(cmd)

      
    @classmethod
    def create(cls,d, conn=None) :
        for f in ("name", "ip", "mac", "source_bridge", "memory", "vcpu", "image", "userid", "pwd"):
            if f not in d:
                raise ValueError("required field '{}' is missing".format(f))


        #first connect to libvirt and get a shell
        if conn is None:
          conn = libvirt.open('qemu:///system')
        if conn is None:
            raise  RuntimeError( 'Failed to establish session with libvirt' )

        if not os.path.exists("/opt/cosim/vm_images/%s"%d["image"]):
            raise ValueError("Specified image %s does not exist, please create teh image.." %"/opt/cosim/vm_images/%s"%d["image"] )

        # create a configuratio from the template
        _config = QemuHost.domain_config_template
        _config = _config.replace( "$MAC_ADDR", d['mac'])
        _config = _config.replace( "$DOMAIN_NAME", d['name'])
        _config = _config.replace( "$DOMAIN_IMG", d['image'])
        _config = _config.replace( "$MEMORY", d['memory'])
        _config = _config.replace( "$VCPUS", d['vcpu'])
        _config = _config.replace( "$SRC_BRIDGE", d['source_bridge'])


        # Check to make sure that the source bridge exists
        bridges = subprocess.check_output("ovs-vsctl show", stderr=subprocess.STDOUT, shell=True)
        if 'Bridge %s'%d['source_bridge'] not in str(bridges):
            raise RuntimeError('Supplied bridge %s is not configured, please configure the bridge before invoking create'%d['source_bridge'])


        
        # check if the instance with the same name already exists
        # if so, exit 
        for domain in conn.listAllDomains():
            #domain = conn.lookupByID(id)
            if domain.name() == d['name']:
                if domain.isActive():
                    domain.destroy() 
                domain.undefine() 

        #instances = conn.listDefinedDomains()
        #if d['name'] in instances:
            # TODO: destroy and undefine domain ??

            #raise RuntimeError( ' Supplied domain name %s already exists, please provide an unique name' % d['name'])

        
        # create instance
        instance = conn.defineXML( _config)
        if instance is None:
            conn.close()
            raise RuntimeError( 'failed to define domain')

        # create instance 
        instance.create()
        dom = conn.lookupByName( d['name'])
        while dom.state()[0] != libvirt.VIR_DOMAIN_RUNNING:
            sleep(1)
        
        console = None
        enable_console = False
        if enable_console:
            try:
                console = QemuConsole(d['name'])
                console.connect()
            except Exception as ex:
                logging.error( "Shutting down guest %s" % self.name)

        # Create a class snd return
        q_host = cls(d["name"], console ,conn, dom, d['userid'], d['pwd'],d['ip'],d['mac'])
        return q_host

    def cmd( self , cmd_line ) :
        if self.console is None:
          return None
        
        return self.console.cmd_output(cmd_line)

    def stop(self):

        '''
        for dom in conn.listAllDomains():
            if dom.name() == self.name:
                if dom.isActive():
                    dom.destroy() 
                dom.undefine() 
        '''
        if self.dom is not None:
            state = self.dom.info()[0]
            if state == libvirt.VIR_DOMAIN_RUNNING:
              logging.info( "Shutting down guest %s" % self.name)
              self.dom.shutdown()
              while self.dom.state()[0] != libvirt.VIR_DOMAIN_SHUTOFF:
                time.sleep(1) 
              self.dom.undefine() 

        # first disconnect from console
        if self.conn is not None:
            self.conn.close()

    def pause(self):
        if self.dom is not None:
            self.dom.suspend()

    def resume(self):
        if self.dom is not None:
            self.dom.resume()




