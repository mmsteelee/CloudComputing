import json
from operator import add
from os import read
from kafka import KafkaProducer
from pyspark.sql import SparkSession
import couchdb
from time import sleep


producer = KafkaProducer (bootstrap_servers="129.114.26.148:30000", value_serializer=lambda v: json.dumps(v).encode('ascii'))
producer.config


if __name__ == "__main__":

    spark = SparkSession\
        .builder\
        .appName("EnergyMapReduce")\
        .getOrCreate()

    sc = spark.sparkContext

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

    for docid in db.view('_all_docs'):
        doc = db[docid['id']]['docs']
        data = data + doc
    
    rdd = sc.parallelize(data)
#    print(rdd.collect())

    sums = rdd.map(lambda x: ((x['house_id'], x['household_id'], x['plug_id']), (float(x['value']), 0.0, 1, 0) if x['property'] == '0' else (0.0, float(x['value']), 0, 1))) \
              .reduceByKey(lambda a,b : (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3]))
    output = sums.collect()

    count = 0
    for (plug_id, values) in output:
        count += 1
        dict  = {'plug_id' : plug_id, 'avg_work' : values[0] / values[2], 'avg_load' : values[1] / values[3]}
        json_dict = json.dumps(dict)
        producer.send('utilizations', json_dict)
        if count % 100 == 0 :
            print('finished: ' + str(count))

    print('All data sent to CouchDB')
    producer.close()
    spark.stop()

