from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("PythonMapReduce")\
        .getOrCreate()

lines = 