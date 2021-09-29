import couchdb
import json
import time # for sleep
from kafka import KafkaConsumer  # consumer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the consumer
# (you will need to change this to your bootstrap server's IP addr)
consumer = KafkaConsumer (bootstrap_servers="129.114.27.112:9092",
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
    couch = couchdb.Server("http://129.114.26.148:5984")
    db = couch[<our db name>]
    db_entry = json.load(msg.value)
    db.save(db_entry)

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close ()
    
