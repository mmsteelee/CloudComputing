README-PA3

Team 10

Manually resized VM2 to m1.medium, also changed the createVMs to make VM2 m1.medium
added playbook to install docker and Kubernetes on ChameleonVMs
wrote playbook to download docker and kubernetes dependencies

then ssh'd into the vms to manually finish installation process
- sudo nano etc/hosts and added aliases for each vm
	- vm2: kubemaster, kubeworker1
	- vm3: kubeworker2
- on VM2: sudo kubeadm init --apiserver-advertise-address 129.114.26.148 --control-plane-endpoint 129.114.26.148 --node-name kubemaster --pod-network-cidr=10.244.0.0/16

K8

On vm2 

sudo swapoff -a

sudo kubeadm reset

sudo kubeadm init --node-name kubemaster --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config