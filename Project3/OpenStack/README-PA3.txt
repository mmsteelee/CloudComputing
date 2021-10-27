README-PA3

Team 10

Manually resized VM2 to m1.medium, also changed the createVMs to make VM2 m1.medium
added playbook to install docker and Kubernetes on ChameleonVMs

K8

On vm2 

sudo swapoff -a

sudo kubeadm reset

sudo kubeadm init --node-name kubemaster --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config


