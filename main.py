import io
import os
import string
from logging import Logger

import dbutils as dbutils
from pandas._typing import Level
from pyspark.sql.functions import col
from pyspark.shell import spark
from pyspark.sql import SQLContext, SparkSession

from pyspark.sql.types import *
from pyspark import SparkConf, SparkContext, SparkFiles
from pyspark.sql import HiveContext
import pyspark.sql.functions as sqf


spark = SparkSession.builder.master('local[*]').appName('venv').config("spark.files.overwrite", "true")\
    .config("spark.worker.cleanup.enabled","true").getOrCreate()
sc = spark.sparkContext
url = "https://physionet.org/files/mimicdb/1.0.0/055/05500001.txt"
sc.addFile(url)


# first get all lines from file
with open(SparkFiles.get("05500001.txt"), 'r') as f:
   lines = f.readlines()

# remove spaces
lines = [line.replace(' ', '') for line in lines]

# finally, write lines in the file
with open("temp.txt", 'w') as f:
    f.writelines(lines)


schema = StructType([
    StructField("Name",StringType(),True),
    StructField("val1",StringType(),True),
    StructField("val2",StringType(),True),
    StructField("val3", StringType(), True)])


readfrmfile = spark.read.csv("temp.txt", header="false", schema=schema, sep='\\t').cache()

readfrmfile = readfrmfile.filter(col('val1').isNotNull())
readfrmfile.show()

rows = readfrmfile.select('Name').distinct().collect()
rowarray = [str(row.Name) for row in rows]

dfArray = [readfrmfile.where(readfrmfile.Name == i) for i in rowarray]

pandasdf = dfArray.toPandas()
os.remove("temp.txt")




