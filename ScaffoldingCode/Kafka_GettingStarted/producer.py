import csv # need this to interact with file
from time import sleeo
from json import dumps
from kafka import KafkaProducer  # producer of events

# acquire the producer
producer = KafkaProducer (bootstrap_servers="129.114.27.112:9092", 
                                          value_serializer=lambda x:
                                          dumps(x).encode('utf-8'))

# open csv file into a reader
with open('Count_Statistics_2019.csv', r) as csv_file:
    csv_reader = csv_reader(csv_file)

# process csv line by line
for line in csv_reader:
    process = line

    # store data as json pair
    contents = {'test_data' : line}

    # send the contents under topic utilizations. contents sent as json pair
    producer.send ("utilizations", value=contents)
    producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep (5)

# we are done
producer.close ()
