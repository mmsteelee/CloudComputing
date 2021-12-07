
# Author: Camren Hall, Safet Hoxha, Luke Garrett
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 22, 2020
#
# Purpose:
#    Use Kafka consumer API to stream data to CouchDB

import json
import couchdb
import csv

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

with open('energy-data.csv', 'w', encoding='UTF8') as csvfile:
    writer = csv.writer(csvfile)
    
    for docid in db.view('_all_docs'):
        data = db[docid['id']]['docs']
        for line in data:
            writer.writerow([line['id'],line['timestamp'],line['value'],line['property'],line['plug_id'],line['household_id'],line['house_id']])
        break
    