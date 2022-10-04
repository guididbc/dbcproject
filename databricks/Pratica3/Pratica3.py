# Databricks notebook source
# MAGIC %run "../Pratica3/configuration"

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

df = spark.read.format("csv")\
.option("inferSchema", True)\
.option("header", True)\
.option("delimiter", ",")\
.option("timestampFormat",'DD/MM/-yyyy hh:mm:ss')\
.load(f"{file_path_orin}")

# COMMAND ----------

df.printSchema()

# COMMAND ----------

display(df)

# COMMAND ----------

display(df)

# COMMAND ----------

temp_invoiced = df.filter(col("order_status") == "invoiced").createOrReplaceTempView("Orders_invoiced")

# COMMAND ----------

df_invoiced = spark.table('Orders_invoiced')

# COMMAND ----------

# MAGIC %sql
# MAGIC use db

# COMMAND ----------

display(df_invoiced)

# COMMAND ----------

type(df_invoiced)

# COMMAND ----------

df_invoiced.write.mode("overwrite").format("delta").saveAsTable("invoiced")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM Orders_invoiced

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS DB
# MAGIC LOCATION "/FileStore/tables/pratica/DB"

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP DATABASE DB

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW DATABASES

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT CURRENT_DATABASE() 

# COMMAND ----------

# MAGIC %sql
# MAGIC Describe DATABASE db
# MAGIC LOCATION ""

# COMMAND ----------

df_tabela =  spark.table('db.invoiced')

# COMMAND ----------

display(df_tabela)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM db.invoiced

# COMMAND ----------

# MAGIC %sql
# MAGIC use default
