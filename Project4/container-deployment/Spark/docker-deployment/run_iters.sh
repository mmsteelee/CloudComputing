#!/bin/sh
i=0
while [ $i -lt 20 ]
do
    ${SPARK_HOME}/bin/spark-submit --master spark://spark-master-svc:7077 --properties-file ${SPARK_HOME}/conf/spark-driver.conf energy-map.py
    
    i=`expr $i + 1`
done
