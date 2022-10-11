# Databricks notebook source
# MAGIC %fs ls "/mnt/adlslearningdbc/silver"

# COMMAND ----------

#%fs ls /FileStore/tables/silver/customers

# COMMAND ----------

# MAGIC %run "../Project/configuration"

# COMMAND ----------

# MAGIC %run "../Project/functions"

# COMMAND ----------

file_path = (f"{silver_folder_path}/customers/*")

# COMMAND ----------

df = spark.read.parquet(file_path)

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.withColumnRenamed("customer_id","customerId").withColumnRenamed("customer_city","city").withColumnRenamed("customer_state","state")

# COMMAND ----------

display(df)

# COMMAND ----------

df.createOrReplaceTempView("customers")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers

# COMMAND ----------

df_sql = spark.sql("\
                SELECT id , customerId, city, state, state as UF  FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY customerId ORDER BY customerId DESC) AS conta\
                               FROM customers) WHERE conta = 1")

# COMMAND ----------

type(df_sql)

# COMMAND ----------

display(df_sql)

# COMMAND ----------

df_sql.write.partitionBy("UF").mode("overwrite").parquet(f"{gold_folder_path}/dimensao/dimcustomers")

# COMMAND ----------

# MAGIC %fs ls /FileStore/tables/gold/dim/customers

# COMMAND ----------

# MAGIC %sql
# MAGIC Create database IF NOT EXISTS OLIST

# COMMAND ----------

# MAGIC %sql
# MAGIC USE olist

# COMMAND ----------

df_sql.write.mode("overwrite").format("parquet").saveAsTable("dimCustomers")
