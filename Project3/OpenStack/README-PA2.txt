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


creation of vms: host: mylocalvm, remote user: vagrant
actions in the cloud vms: host: mychameleonvms, remote user: cc

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
Matt & Brett - help troubleshooting ansible configuration and initial research into playbook writing

Effort expended: 
- most time consuming part of milestone 1 was the time it takes to destroy/recreate the vagrant vm when the vagrantfile is not complete or has bugs


M2:

Instantiating the openstack VM's through ansible playbooks (CreateVMs.yml).
- specifying cloud: openstack after using openstack accessibility to chameleon vms
- ubuntu 20.04 image
- our team private key for ssh access (linked via .ansible.cfg from vagrant vm)
- m1.small flavors for both vm2 and vm3
- enabling security groups for each; same groups as found in PA1
- assign floating ip's

We had difficulty with ssh ing into the vms, however this was fixed with an error in the ansible.cfg file.
- had been trying to reference the private key from my laptop, not the vagrant vm

Downloading Kafka by using yaml language to call apt update, upgrade, and installation
- had to install javajdk here first, then remove old kafka dir, before making new kafka dir
- download kafka file and extract it into vms

Then we edited the server.properties files for both VMs which was pretty simple using ansibles replace module and changing the broker ids, listenerst etc.
Starting the zookeeper and kafka servers were also trivial as it was the same commands used in project 1:
    - shell: 'bin/zookeeper-server-start.sh config/zookeeper.properties'
    - shell: 'bin/kafka-server-start.sh config/server.properties'

Creating the utilizations topic was also simple in a ansible playbook by using the shell command
    shell: "bin/kafka-topics.sh --create --topic utilizations --bootstrap-server localhost:9092"

Consumer code was copied from the vagrant VM into VM3 via a playbook and executed in python in another playbook.

Teamwork:
Austin:
- owns/runs vagrant vm for debugging ansible runs and each playbook
- wrote master playbook and formatted /tasks dir
Matt: 
- wrote playbooks to 
	- set UFW rules for vms
	- configure server.properties for both vms
	- set up and run kafka servers
	- copying/starting consumer code in vm3
- troubleshooting kafka server configurations
Brett:
- did background research into how yaml files are/need to be written

Effort Expended:
- our process was slowed signifigantly with issues ssh'ing into the vms due to the issue with the .ansible.cfg file referencing the wrong location for the private key for the vms
- once this was resolved, the next major issue was trying to figure out how to write in yaml lang to write the playbooks
- the scaffolding code helps, but is not nearly comprehensive enough to learn how to write commands in the playbooks
- links to ansible documentation gives ideas, but the trial and error to get the playbooks running was incredibly time consuming
	- particularly for the master playbook and vm creation playbooks, as these commands take time to run. vms need to be destroyed and recreated if the playbook did not work as intended

M3: couchdb
playbook written to download couchdb runs a shell script to call initial installation commands
- enabling couchdb repo
installation via apt update, upgrade
couchdb configuration by copying local.ini file to create the admin user & change permissions

- see what she says re: couchdb and PA2, 
- then beginning of meeting tomorrow record vid of producer code -- consumer code stuff w/ or w/o couchdb based on what TA says

Teamwork:
Austin: debugging each playbook on vagrant vm
Matt: wrote downloadcouchdb playbook
Brett: research into ansible documentation as to what commands are needed in each playbook to complete tasks

Effort Expended:
- Downloading Couchdb took a lot of trial and error, as we had difficulty downloading it with the depricated libraries on the last project
- tried new approach using a .sh file to run the commands to download couchdb and copying our local.ini file into the correct path.
- errors:
	- malformed entry with couchdb install - see line in install-cdb.sh
	- local.ini file format/content; for now its mostly scaffolding we found online
		- we never wrote this for PA1 as we never got the couchdb download to work
- potentially syntactic errors?