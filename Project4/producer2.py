import csv # need this to interact with file
import time
from json import dumps
from kafka import KafkaProducer  # producer of events

# acquire the producer
producer = KafkaProducer(bootstrap_servers="129.114.26.148:30000",
                                          value_serializer=lambda x:
                                          dumps(x).encode('utf-8'))

# open csv file into a reader
with open('energy-sorted2.csv') as csv_file:
    csv_reader = csv.reader(csv_file)

# process csv line by line
empty = False

while not empty:
    line = ""
    contents = []

    for i in range(1000):
        line = csv_reader.next()
        if not line:
            empty = True
            break
        dict = {'id': line[0], 'timestamp': line[1], 'value': line[2],
                'property': line[3], 'plug_id': line[4], 'household_id': line[5], 'house_id': line[6]}
        contents.append(dict)



    if not empty:
        contents = {'energy_data': contents}
        # send the contents under topic utilizations. contents sent as json pair
        producer.send ("utilizations", value=contents)
        producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep (5)

# we are done
producer.close ()
