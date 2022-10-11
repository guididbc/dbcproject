# Databricks notebook source
# MAGIC %fs ls "/mnt/adlslearningdbc/bronze/project"

# COMMAND ----------

#%fs ls "/FileStore/tables/bronze/customers"

# COMMAND ----------

#%fs rm -r /FileStore/tables/

# COMMAND ----------

# MAGIC %run "../Project/configuration"

# COMMAND ----------

# MAGIC %run "../Project/functions"

# COMMAND ----------

file_path = (f"{bronze_folder_path}/olist_customers_dataset/*")

# COMMAND ----------

df = spark.read.parquet(f"{bronze_folder_path}/olist_customers_dataset/*")

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.select(col("customer_id"),col("customer_city"),col("customer_state"))

# COMMAND ----------

display(df)

# COMMAND ----------

df = add_date_process(df)

# COMMAND ----------

display(df)

# COMMAND ----------

df = df.withColumn("id",monotonically_increasing_id()+1).withColumn("UF",col("customer_state"))

# COMMAND ----------

display(df)

# COMMAND ----------

df.write.partitionBy("UF").mode("overwrite").parquet(f"{silver_folder_path}/customers")

# COMMAND ----------

# MAGIC %fs ls "/FileStore/tables/silver/customers"

# COMMAND ----------

# MAGIC %fs rm -r "/FileStore/tables/silver/customers"
