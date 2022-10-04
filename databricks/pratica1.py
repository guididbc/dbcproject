# Databricks notebook source
# DBTITLE 1,Getting dbfs
# MAGIC %fs ls /FileStore/tables/pratica

# COMMAND ----------

# DBTITLE 1,Remove DBFS
#%fs rm -r /FileStore/tables/pratica/delivered

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

# DBTITLE 1,Variable path
file_path = "/FileStore/tables/pratica/olist_orders_dataset.csv"
file_path_invoiced = "/FileStore/tables/pratica/invoiced"
file_path_delivered  = "/FileStore/tables/pratica/delivered"

# COMMAND ----------

type(file_path_invoiced)

# COMMAND ----------

# DBTITLE 1,Reading csv file
df = spark.read.format("csv")\
.option("inferSchema", True)\
.option("header", True)\
.option('delimiter', ',')\
.load(file_path)

# COMMAND ----------

type(df)

# COMMAND ----------

# DBTITLE 1,Show me 100 rows
#show me 100 rows
display(df.limit(100))

# COMMAND ----------

# DBTITLE 1,Filtering invoiced status
display(df.filter(col("order_status") == "invoiced"))

# COMMAND ----------

# DBTITLE 1,Filtering invoiced status
display(df.where(col("order_status") == "delivered"))

# COMMAND ----------

# DBTITLE 1,Storing the filter in DF
df_invoiced = df.filter(col("order_status") == "invoiced")

# COMMAND ----------

display(df_invoiced)

# COMMAND ----------

# DBTITLE 1,Storing the filter in DF
df_delivered = df.where(col("order_status") == "delivered")

# COMMAND ----------

display(df_delivered)

# COMMAND ----------

df_invoiced.write.option("header", True).option("delimiter",",").mode("overwrite").csv(file_path_invoiced)
df_delivered.write.option("header", True).option("delimiter",",").mode("overwrite").csv(file_path_delivered)
