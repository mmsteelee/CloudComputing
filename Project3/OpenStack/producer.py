import json
import os   # need this for popen
import time # for sleep
from kafka import KafkaProducer  # producer of events
import csv

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="129.114.27.112:30001", value_serializer=lambda v: json.dumps(v).encode('ascii'))

with open("national-history.csv", mode='r') as infile:
    reader = csv.reader(infile)

# say we send the contents 100 times after a sleep of 1 sec in between
    for row in reader:
    
    # get the output of the top command
    # read the contents that we wish to send as topic content
   # contents = "bill clinton"

    # send the contents under topic utilizations. Note that it expects
    # the contents in bytes so we convert it to bytes.
    #
    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #
    #producer.send ("hghdata", value=bytes (contents, 'ascii' ))i
        dict = {'date' : row[0], 'death' : row[1], 'deathIncrease' : row[2], 'inIcuCumulative' : row[3],
                   'inIcuCurrently' : row[4], 'hospitalizedIncrease' : row[5], 'hospitalizedCurrently' : row[6],
                   'hospitalizedCurrently' : row[7], 'negative' : row[8], 'negativeIncrease' : row[9],
                   'onVentilatorCumulative' : row[10], 'onVentilatorCurrently' : row[11], 'positive' : row[12],
                   'positiveIncrease' : row[13], 'states' : row[14], 'totalTestResults' : row[15],
                   'totalTestResultsIncrease' : row[16]}
        json_dict = json.dumps(dict)
        producer.send('utilizations', json_dict)
        producer.flush ()   # try to empty the sending buffer
        time.sleep(0.1)

# we are done
producer.close ()
