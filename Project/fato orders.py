# Databricks notebook source
# MAGIC %fs ls "/mnt/adlslearningdbc/silver"

# COMMAND ----------

from pyspark.sql.window import *
from pyspark.sql.functions import *

# COMMAND ----------

# MAGIC %run "../Project/Connection"

# COMMAND ----------

# MAGIC %run "../Project/configuration"

# COMMAND ----------

# MAGIC %run "../Project/functions"

# COMMAND ----------

file_path_orders = (f"{silver_folder_path}/orders/*")
file_path_status = (f"{gold_folder_path}/dimensao/dimstatus/*")
file_path_customers = (f"{gold_folder_path}/dimensao/dimcustomers/*")

# COMMAND ----------

df_orders = spark.read.parquet(file_path_orders)\
.withColumnRenamed("order_id", "IdOrder")\
.withColumnRenamed("customer_id", "IdCustomer")\
.withColumnRenamed("order_status", "Status")\
.withColumnRenamed("order_purchase_timestamp", "DtCompra")\
.withColumnRenamed("order_approved_at", "DataAprovacao")\
.withColumnRenamed("order_delivered_carrier_date", "EntregaLogis")\
.withColumnRenamed("order_delivered_customer_date", "EntregaCliente")\
.withColumnRenamed("order_estimated_delivery_date", "EstimativaEntrega")\
.withColumn("status_p",(col("Status")))

# COMMAND ----------

df_status = spark.read.parquet(file_path_status)

# COMMAND ----------

df_customers = spark.read.parquet(file_path_customers)

# COMMAND ----------

display(df_orders)

# COMMAND ----------

display(df_status)

# COMMAND ----------

# DBTITLE 1,Join
df_join = df_orders.join(df_status, df_orders.Status == df_status.order_status, "left")\
.select(df_orders.id,df_orders.IdOrder,df_orders.IdCustomer,df_status.id.alias("skStatus"),df_orders.DtCompra,df_orders.DataAprovacao,df_orders.EntregaLogis,df_orders.EntregaCliente,df_orders.EstimativaEntrega,df_orders.status_p)

# COMMAND ----------

# DBTITLE 1,Join 2
df_join = df_join.join(df_customers, df_join.IdCustomer == df_customers.customerId, "left")\
.select(df_orders.id,df_orders.idOrder,df_customers.id.alias("skCustomer"),df_join.id.alias("skStatus"),df_orders.DtCompra,df_orders.DataAprovacao,df_orders.EntregaLogis,df_orders.EstimativaEntrega,df_orders.EntregaCliente,df_orders.status_p)

# COMMAND ----------

display(df_join)

# COMMAND ----------

#df = df.select(col("id"),col("idOrder"),col("IdCustomer"),col("Status"),col("DtCompra"),col("DataAprovacao"),col("EntregaLogis"),col("EstimativaEntrega"),col("EntregaCliente"), col("status_p"))

# COMMAND ----------

df_join.write.partitionBy("status_p").mode("overwrite").parquet(f"{gold_folder_path}/fato/fatoOrders/")

# COMMAND ----------

# MAGIC %sql
# MAGIC USE OLIST

# COMMAND ----------

df_join.write.mode("overwrite").format("parquet").saveAsTable("FatoOrders")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fatoorders
