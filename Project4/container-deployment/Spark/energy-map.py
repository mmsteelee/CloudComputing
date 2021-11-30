from pyspark.sql import SparkSession
import couchdb

spark = SparkSession\
        .builder\
        .appName("PythonMapReduce")\
        .getOrCreate()

ip_couchdb = "129.114.27.112"
user = "admin"
password = "cloud"
couch = couchdb.Server("http://{}:{}@{}:30006".format(user, password, ip_couchdb))
dbname = "energy-data"
db = couch[dbname]

lines = 