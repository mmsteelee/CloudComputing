import csv # need this to interact with file
from time import sleeo
from json import dumps
from kafka import KafkaProducer  # producer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="129.114.27.:9092", 
                                          value_serializer=lambda x:
                                          dumps(x).encode('utf-8'))  # wait for leader to write to log

# say we send the contents 100 times after a sleep of 1 sec in between
with open('Count_Statistics_2019.csv', r) as csv_file:
    csv_reader = csv_reader(csv_file)

for line in csv_reader:
    process = line

    contents = {'test_data' : line}

    # send the contents under topic utilizations. Note that it expects
    # the contents in bytes so we convert it to bytes.
    #
    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #
    producer.send ("utilizations", value=contents)
    producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep (5)

# we are done
producer.close ()
