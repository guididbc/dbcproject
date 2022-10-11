# Databricks notebook source
# MAGIC %fs ls "/mnt/adlslearningdbc/silver/orders"

# COMMAND ----------

# MAGIC %fs ls /FileStore/tables/gold/dim/status

# COMMAND ----------

#%fs ls /FileStore/tables/gold/dim/status

# COMMAND ----------

# MAGIC %run "../Project/Connection"

# COMMAND ----------

# MAGIC %run "../Project/configuration"

# COMMAND ----------

# MAGIC %run "../Project/functions"

# COMMAND ----------

from pyspark.sql.window import *
from pyspark.sql.functions import *

# COMMAND ----------

file_path = (f"{silver_folder_path}/orders/*")

# COMMAND ----------

df = spark.read.parquet(file_path)

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.select(col("order_status"))

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.groupBy("order_status").count().withColumn("id", monotonically_increasing_id()+1)

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.select(col("order_status"), col("id"))

# COMMAND ----------

display(df)

# COMMAND ----------

df.write.mode("overwrite").parquet(f"{gold_folder_path}/dimensao/dimstatus")

# COMMAND ----------

#%fs rm -r /FileStore/tables/gold

# COMMAND ----------

# MAGIC %sql
# MAGIC Create database if not exists olist

# COMMAND ----------

# MAGIC %sql
# MAGIC use olist

# COMMAND ----------

df.write.mode("overwrite").format("parquet").saveAsTable("dimStatus")
