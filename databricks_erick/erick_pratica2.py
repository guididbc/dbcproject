# Databricks notebook source
# MAGIC %fs ls /FileStore/tables/pratica_erick/

# COMMAND ----------

# DBTITLE 1,Importing Libraries
from pyspark.sql.functions import *
from pyspark.sql.types import *


# COMMAND ----------

file_path = "/FileStore/tables/pratica_erick/olist_customers_dataset.csv"

# COMMAND ----------

type(file_path)

# COMMAND ----------

df = spark.read.format("csv")\
    .option("inferSchema",True)\
    .option("header",True)\
    .option("delimiter",",")\
    .load(file_path)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df_schema = StructType([
    StructField("customer_id", StringType()),
    StructField("customer_unique_id", StringType()),
    StructField("customer_zip_code_prefix", StringType()),
    StructField("customer_city", StringType()),
    StructField("customer_state", StringType()),
])

# COMMAND ----------

type(df_schema)

# COMMAND ----------

df = spark.read.format("csv")\
    .option("header",True)\
    .schema(df_schema)\
    .option("delimiter",",")\
    .load(file_path)

# COMMAND ----------

df.printSchema()
