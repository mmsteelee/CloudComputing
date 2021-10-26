README-PA2

Team 10

Setup: 

downloaded vagrant with ubuntu 20.04 box image --> ubuntu/focal64
configured VangrantFile:
config.vm.provider for virtualbox, gui = true
configure.vm.provision "shell", path: "bootstrap.sh"
config.vm.provision "file", source: 'path to my .pem ssh'
began copying ansible.cfg
config.vm.provision "file", source: 'path to .ansible.cfg'
config.vm.provision "file", source: 'path to MyInventory'
setup vagrant to communicate with chameleon VMs
this line was commented out of Vagrantfile to allow for creation of VM
config.vm.provision "file", source: "C:/Users/awggs/.config/openstack/clouds.yaml", destination: "~/.config/openstack/clouds.yaml"

Using the new VM
- no way into it via the gui that pops up, no sign in info
use vangrant ssh, signs into vagrant@ubuntu-focal using the ssh .pem provided in Vagrantfile
using ansible as provisioner to install packages on the machine, installing ansible in
Vagrantfile:
ansible.playbook = 'master_demo_playbook'
ansible.install = true

MyInventory file
- change to IP for the cloud VMs. different sections for chameleon VMs and AWS VMs

.ansible.cfg file
- directed to MyInventory path, private key file, and python env in the vagrant VM

copy MyInventory to the new ansible directory
# cp MyInventory ~/.ansible/

which python3 shows /usr/bin/python3
which ansible shows usr/bin/ansible
sudo apt install pip
ansible-galaxy collection install openstack.cloud
sudo python3 -m pip  install --upgrade openstacksdk


to try playbooks (for milestone 1):
cd /vagrant/
ls -a will show all files in the same directory as Vagrantfile
ansible-playbook <playbook>.yml
- runs with errors for access to chameleon VMs, but running/accessing the playbooks
- themselves works

once everything is loaded:
vagrant provision

Teamwork M1:
Austin - setup and running vagrant as local VM
Matt & Brett - help troubleshooting ansible configuration and playbook writing

creation of vms: host: mylocalvm, remote user: vagrant
actions in the cloud vms: host: mychameleonvms, remote user: cc

M2&3:


