import json
import os   # need this for popen
from kafka import KafkaConsumer  # consumer of events
import couchdb

ip_kafka = "129.114.26.148"
ip_couchdb = "129.114.27.112"
consumer = KafkaConsumer (bootstrap_servers="{}:30000".format(ip_kafka), value_deserializer=lambda v: json.loads(v).encode('ascii'))

consumer.subscribe (topics=["utilizations"])

# acquire couchdb server
user = "admin"
password = "admin"
conn_string  = "http://{}:{}@{}:30006".format(user, password, ip_couchdb)
print(conn_string)
couch = couchdb.Server(conn_string)
dbname = "team10-data"

if dbname in couch:
    db = couch[dbname]
else:
    db = couch.create(dbname)

# we keep reading and printing
for msg in consumer:
    print (msg.value)
    document = json.loads(msg.value)
    #db.save(msg.value)
    #db.save({'type': 'Person', 'name': 'John Doe'})
    db.save(document)
consumer.close ()
    