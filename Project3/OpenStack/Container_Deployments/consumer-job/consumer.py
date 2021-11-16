import json
import os   # need this for popen
from kafka import KafkaConsumer  # consumer of events
import couchdb

ip_kafka = "129.114.26.148"
ip_couchdb = "129.114.27.112"
consumer = KafkaConsumer (bootstrap_servers="{}:30002".format(ip_kafka), value_deserializer=lambda m: json.loads(m.decode('utf-8')))

consumer.subscribe (topics=["utilizations"])

# acquire couchdb server
user = "admin"
password = "cloud"
couch = couchdb.Server("http://{}:{}@{}:30006".format(user, password, ip_couchdb))
dbname = "team10-data"

if dbname in couch:
    db = couch[dbname]
else:
    db = couch.create(dbname)

# we keep reading and printing
for msg in consumer:
    # print(msg.value)
    # document = json.load(msg.value)
    document = {'test': str(msg.value, 'ascii')}
    # db.save(msg.value)
    db.save(document)
consumer.close()
