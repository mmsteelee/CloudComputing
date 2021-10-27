README-PA3

Team 10

Manually resized VM2 to m1.medium, also changed the createVMs to make VM2 m1.medium
added playbook to install docker and Kubernetes on ChameleonVMs

K8

K8

sudo ufw limit 10255
sudo ufw limit 10256

On vm2 

sudo swapoff -a

sudo kubeadm reset

sudo kubeadm init --node-name kubemaster --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

kubeadm token create --print-join-command

VM3

Use the join command printed out by the command above

VM2 tainting master:

Apt-get install jq

kubectl get nodes -o json | jq '.items[].spec.taints'

kubectl taint nodes kubemaster node-role.kubernetes.io/master:NoSchedule