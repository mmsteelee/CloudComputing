import json
from operator import add
from os import read
from kafka import KafkaProducer
from pyspark.sql import SparkSession
import couchdb
from time import sleep
import csv


producer = KafkaProducer (bootstrap_servers="129.114.26.148:30000", value_serializer=lambda v: json.dumps(v).encode('ascii'))
producer.config


if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()

    sc = spark.sparkContext


    # acquire couchdb server
    ip_couchdb = "129.114.27.112"
    user = "admin"
    password = "cloud"
    conn_string  = "http://{}:{}@{}:30006".format(user, password, ip_couchdb)
    print(conn_string)
    couch = couchdb.Server(conn_string)
    dbname = "energy-data"

    if dbname in couch:
        db = couch[dbname]
    else:
        db = couch.create(dbname)

    data = []
    with open('energy-data.csv', 'r', encoding='UTF8') as f: 
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    
    rdd = sc.parallelize(data)
#    print(rdd.collect())

    sums = rdd.map(lambda x: ({'house_id' : x[6], 'household_id' : x[5], 'plug_id' : x[4]}, (float(x[2]), 0.0) if x[3] == '0' else (0.0, float(x[2])))) \
              .reduceByKey(lambda a,b : (a[0] + b[0], a[1] + b[1]))
    output = sums.collect()

    for (household, values) in output:
        print({household : values})
#        json_dict = json.dumps(dict)
#        producer.send('utilizations', json_dict)

    producer.close()
    spark.stop()

