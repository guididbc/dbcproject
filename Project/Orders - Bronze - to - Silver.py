# Databricks notebook source
# MAGIC %fs ls "/mnt/adlslearningdbc/bronze/project"

# COMMAND ----------

#%fs ls /FileStore/tables/bronze/orders

# COMMAND ----------

# DBTITLE 1,Importing Libries
from pyspark.sql.window import *
from pyspark.sql.functions import *

# COMMAND ----------

# MAGIC %run "../Project/Connection"

# COMMAND ----------

# MAGIC %run "../Project/configuration"

# COMMAND ----------

# MAGIC %run "../Project/functions"

# COMMAND ----------

file_path = (f"{bronze_folder_path}/olist_orders_dataset/*")

# COMMAND ----------

df = spark.read.parquet(file_path)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

display(df)

# COMMAND ----------

df = add_date_process(df)

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.withColumn("status",col("order_status")).withColumn("id", monotonically_increasing_id()+1)

# COMMAND ----------

df.write.partitionBy("status").mode("overwrite").parquet(f"{silver_folder_path}/orders")

# COMMAND ----------

# MAGIC %fs ls /FileStore/tables/silver/orders

# COMMAND ----------

# MAGIC %fs rm -r /FileStore/tables/silver/orders
