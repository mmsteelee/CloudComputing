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

sudo ufw limit 10255
sudo ufw limit 10256
sudo ufw limit 2379:2380/tcp
sudo ufw limit 6443/tcp
sudo ufw limit 10250:10252/tcp
sudo ufw limit 8285/udp
sudo ufw limit 8472/udp
sudo ufw limit 30000:30004/tcp
sudo ufw limit 30005/tcp
sudo ufw limit 30006/tcp


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
sudo apt install jq
kubectl get nodes -o json | jq '.items[].spec.taints'
kubectl taint nodes kubemaster node-role.kubernetes.io/master:NoSchedule-

Deployment:
scp /Users/mattsteele/School/CS\ 4287/CloudComputingCourse/ScaffoldingCode/DockerCluster_wKubernetes/Deployment/nginx-deployment.yaml cc@129.114.26.148:
kubectl apply -f nginx-deployment.yaml
kubectl get deployments
kubectl rollout status nginx-deployment
Viewing results:
kubectl describe deployment nginx-deployment
kubectl get pods --all-namespaces

Job:
docker build -f dockerfile –t my-matinv .
docker run -d -p 5000:5000 –restart=always --name registry registry:2
docker tag my-matinv:latest 129.114.26.148:5000/my-matinv
docker push 129.114.26.148:5000/my-matinv
kubectl apply -f matinv-job_wCorrectRegistry.yaml
View results:
kubectl get pods

# not completed
Service jobs:
docker build -f ./dockerfile_server -t matinv-server .
sudo docker tag matinv-server:latest 129.114.26.148:5000/matinv-server

teamwork:
Austin: troublshot the kubernetes download playbook, configured the clusters, recorded demonstration of deployment and job scaffolding code running on pods in docker
Matt: wrote the kubernetes download playbook
Brett: researched kubernetes and helped troubleshoot configuration issues


Effort expended:
there was confusion in how to get the clusters configured, but once we spent enough time with the scaffolding code and slides 
the deployment and job demonstrations were simple enough. 
there are issues getting service-job to work, involving pushing to the private registries. 

