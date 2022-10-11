# Databricks notebook source
# MAGIC   %fs ls /FileStore/tables/daniel_pratica

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

import pandas as pd
from datetime import datetime, timedelta

# COMMAND ----------

# DBTITLE 1,Variáveis de arquivos
cm_arq_orders =    '/FileStore/tables/daniel_pratica/olist_orders_dataset.csv'
cm_arq_customers = '/FileStore/tables/daniel_pratica/olist_orders_dataset.csv'
cm_arq_payments =  '/FileStore/tables/daniel_pratica/olist_customers_dataset.csv'
grava_invoiced = '/FileStore/tables/daniel_pratica/invoiced'
grava_delivered = '/FileStore/tables/daniel_pratica/delivered'
grava_customers = '/FileStore/tables/daniel_pratica/customers'
grava_payments_sp = '/FileStore/tables/daniel_pratica/payments'
grava_payments_not_sp = '/FileStore/tables/daniel_pratica/payments'

# COMMAND ----------

type("cm_arq_orders")

# COMMAND ----------

df_orders = spark.read.format("csv")\
.option("header", "true")\
.option("inferschema", "true")\
.option("delimiter", ",")\
.load(cm_arq_orders)

# COMMAND ----------

display(df_orders)

# COMMAND ----------

display(df_orders.filter(col("order_status") == "delivered")) 

# COMMAND ----------

df_delivered = df_orders.filter(col("order_status") == "delivered")
display(df_delivered)

# COMMAND ----------

df_invoiced = df_orders.filter(col("order_status")=="invoiced")
df_invoiced.limit(5).toPandas()


# COMMAND ----------

df_invoiced.count()

# COMMAND ----------

display(df_invoiced.selectExpr("order_status as pangare", "order_status"))


# COMMAND ----------

display(df_orders.where(col("order_status")=="canceled"))

# COMMAND ----------

df_customers = spark.read.format("csv")\
.option("header", "true")\
.option("inferschema", "true")\
.option("delimiter", ",")\
.load(cm_arq_customers)
df_customers.limit(10).toPandas()

# COMMAND ----------

df_customers.printSchema()

# COMMAND ----------

# DBTITLE 1,Filtra dados >=2018
 df_cust_filtrado = (df_customers\
.filter('order_approved_at > "2018-01-01 00:00:00" '))
display(df_cust_filtrado)
    

# COMMAND ----------

df_payments = spark.read.format("csv")\
.option("header", "true")\
.option("inferschema", "true")\
.option("delimiter", ",")\
.load(cm_arq_payments)
df_payments.limit(10).toPandas()


# COMMAND ----------

df_payments_SP = df_payments.filter('customer_state == "SP"')
display(df_payments_SP)

# COMMAND ----------

df_payments.createOrReplaceTempView("df_view_payments") 


# COMMAND ----------

df_payments_dif_sp = spark.sql("""
select * from df_view_payments where customer_state <> 'SP'""")
display(df_payments_dif_sp)

# COMMAND ----------

df_invoiced.write.option("header", True).option("delimiter", ",").mode("overwrite").csv(grava_invoiced)
df_delivered.write.option("header", True).option("delimiter", ",").mode("overwrite").csv(grava_delivered)
df_payments_dif_sp.write.option("header", True).mode("overwrite").csv(grava_payments_not_sp)



# COMMAND ----------

# MAGIC %fs ls /FileStore/tables/daniel_pratica
