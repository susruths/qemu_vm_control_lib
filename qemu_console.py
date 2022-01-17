import pexpect
import os
import logging


class QemuConsole:

    def __init__( self, vm_name):
        self.name = vm_name
        self.console = None
        self.prompt = None
        self.connected = False


    def connect(self):
        self.console = pexpect.spawn('virsh -c qemu:///system console %s' % self.name)
        self.console.expect('.*]')
        self.console.sendline('\r')
        i = self.console.expect(['.*login:', 'intel@[^:]+:[^\$]+[#\$] ' ])
        if i == 0:
            logging.info("Logging in to %s ...." % self.name)
            #self.console.expect('.*login:')
            self.console.sendline('intel')
            self.console.expect('.*assword:.*')
            self.console.sendline('intel123')

        i = self.console.expect(['Permission denied', 'Terminal type', 'intel@[^:]+:[^\$]+[#\$] '])
        if i == 2:
            logging.info("Connected to %s ...." % self.name)
            self.prompt = self.console.after.decode("utf-8")
            self.connected = True
    
    def cmd_output(self, cmd):
        
        if self.connected and self.console is not None:
            self.console.sendline(cmd)
            i = self.console.expect(['\[sudo\].*assword[^:]+: ', 'intel@[^:]+:[^\$]+[#\$] '])
            if i == 0:
                self.console.sendline('intel123')
                self.console.expect('intel@[^:]+:[^\$]+[#\$] ')

            return self.console.before.decode('utf-8')
        
        return None

    def exit(self):
        if self.connected and self.console is not None:
            self.console.sendline('exit')
            self.console.expect('.*login:')
            self.console.sendcontrol(']')

