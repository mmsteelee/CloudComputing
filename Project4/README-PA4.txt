README-PA3

Team 10

Milestone 1:

split up provided energy data into 3 parts, 
and wrote producer code corresponding to each file for each team member to use

Effort expended:
- the delay in completing PA3 factored into this milestone being completed, as our issue involved
	our pipeline not being complete, and data not being stored in couchdb
- once that issue was resolved, milestone 1 was very simple

Teamwork:
- Matt: wrote the producer code for each team member, and split up the energy data into 3 csv files
- Austin: recorded the demo video
- Brett: N/A

for demo:
open driver node:
kubectl exec -it spark-driver-deploy-6b4f5885db-wcqpk /bin/bash

tests: 
${SPARK_HOME}/bin/spark-submit --master spark://spark-master-svc:7077 --properties-file ${SPARK_HOME}/conf/spark-driver.conf energy-map.py

for work submissions: 

exec into the kubernetes spark driver pod

nano ${SPARK_HOME}/conf/spark-driver.conf
change the default parralleism and partitions to the map # and reduce #

run the script run_iters.sh by typing ./run_iters.sh

repeat 3 times with the different map and reduce numbers, get data on the time it has taken to do each of the 10 executions of map/reduce and plot the distribution
can access spark web gui at http://129.114.26.148:30008
