import couchdb
import json
import time # for sleep
from kafka import KafkaConsumer  # consumer of events

# acquire the consumer
consumer = KafkaConsumer (bootstrap_servers="129.114.26.148:30006",
                                    value_deserializer=lambda m:
                                    json.loads(m.decode('utf-8')))

# subscribe to topic
consumer.subscribe (topics=["utilizations"])

# we keep reading and printing
for msg in consumer:
    # what we get is a record. From this record, we are interested in printing
    # the contents of the value field. We are sure that we get only the
    # utilizations topic because that is the only topic we subscribed to.
    # Otherwise we will need to demultiplex the incoming data according to the
    # topic coming in.

    # placeholder code for M2
    # print(msg.value)

    # couchdb code for M3
    couch = couchdb.Server("http://129.114.27.112:5984")

    # username/password if necessary
    server.resource.credentials = ("admin", "admin")

    # create db
    if "cdb-db" not in couch:
         couch.create("cdb-db")
    #
    db = couch["cdb-db"]
    db_entry = json.load(msg.value)
    db.save(db_entry)

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close ()
    