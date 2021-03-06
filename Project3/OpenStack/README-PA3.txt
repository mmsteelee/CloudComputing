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
kubeadm token create --print-join-command + --node-name kubeworker2

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


Milestone 2:
automation of k8 initialization, worker node join, and master tainting

when troubleshooting k8 vm2 init:
run sudo kubeadm reset on vm2 before each new init attempt
delete .kube dir: sudo rm -r .kube/

localhost connection error usually means we tried a kube command w/o sudo

Effort expended:
getting the k8 initialization automated was not so bad, but trying to get VM3 to join as a worker took a lot of time.
we couldn't write the init command and the vm3 join in the same task playbook, as it didn't let us switch hosts mid-task,
so we had to find a way to store the join token, concatenate --node-name kubeworker2 at the end, and run that concatenated command.
in the end, we used an external file to store the join token, then echo --node-name edit to a cat call on the variable file, store that as a
local variable, then call it in a shell

copied deployment and service directories (with yml files) into vm2
cd into service first, kubectl apply -f the services (zookeeper, then kafka, then couchdb),
then kubectl apply -f the deployments (kafka, couchdb), then kubectl apply -f the consumer

effort expended:
we were very unfamiliar with writing yaml files, so the process took a lot of time with the professor for help troubleshooting
syntactic errors, port misalignments, etc. for deploying 5 kafka pods that could connect to the zookeeper and couchdb pods

we are still getting an image pull error when trying to run the consumer job deployment,
that code will also be submitted for review/advice here, and follow up on monday

Teamwork:
Matt: writing playbooks for automated k8 initialization, worker join, and master tainting
Austin: troubleshooting the playbooks on the vagrant vm provision. troubleshooting manual pod deployments on VMs
Brett:

Milestone 3:

made a deployment directory to automatically call the kubectl apply -f <...> for each deployment/service

to get couchdb working (for the first time) - changed from service/deployment to just "pod" resource type

producer code edited to send to kafka3 deployment (where the topic was declared) 
consumer code edited to fetch from the ??? to retrieve the data producer is sending, then provided location of couchdb sink (ip of VM3:30006)


effort expended: 

refactored our deployment and services directories into one master directory to simplify remote copy process

finally got automated remote copy working - had been a bug in the path (vagrant/cc/home != vagrant/home/cc)

automated init and join done
- automating deployment not too difficult, but we were still having issues with the couchdb and consumer pods throwing errors
- finally fixed the couchdb issue, and got the gui working - helped troublshoot consumer code
- it was tricky getting the producer and consumer code to send to the correct kafka deployment pod

full pipline working:
- had been having issues getting data saved in couchdb, even when all pods were running successfully
- had to manually create dockerfiles for kafka deployment, zookeeper deployment, and consumer deployment. 
- reduced kafka deployment to 2 clusters: one on each vm

teamwork:
- Austin: troubleshooting automated deployment process with vagrant vm, management of cloud vms and clusters,
	 recorded demo video
- Matt: wrote dockerfiles and refactored ansible playbook code. did much of the troubleshooting after 
	the big hurdle with no data being saved in couchdb was encountered
- Brett: N/A