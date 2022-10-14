# Databricks notebook source
# DBTITLE 1,Importando Bibliotecas
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, IntegerType ## seleciona algumas bibliotecas de Types
from pyspark.sql.types import * ## seleciona todas as bibliotecas de Types
import pandas as pd

# COMMAND ----------

# DBTITLE 1,Buscar caminho do outro notebook
### vai em REPO ou onde o notebook está armazenado e clica com o botão direto no notebook que vai ser chamado. copia o aminho e depois remove do caminho o 'Databricks'###

# COMMAND ----------

# DBTITLE 1,Chamar outro notebook 
# MAGIC %run "../Daniel_P3/configp3" 

# COMMAND ----------

# DBTITLE 1,Imporatndo arquivo CSV
df = spark.read.format("csv")\
.option("inferSchema", True)\
.option("header", True)\
.option("delimiter", ",")\
.option("timestampFormat","")\
.load(caminho_ori)
display(df)

# COMMAND ----------

df.filter('order_purchase_timestamp >= "[dt_var]" ').toPandas()


# COMMAND ----------

display(df)

# COMMAND ----------

# DBTITLE 1,Criando uma Temp View
df.createOrReplaceTempView("orders")
type('orders')

# COMMAND ----------

# DBTITLE 1,Criando um dataframe a partir de um comando sql

df_sql = spark.sql(""" 
select 
order_id,
customer_id,
order_status,
order_purchase_timestamp
from orders where order_purchase_timestamp >='2018-01-05 13:34:35'  """)
display(df_sql)


# COMMAND ----------

# DBTITLE 1,verificando o database que está conctado
# MAGIC %sql
# MAGIC select current_database()

# COMMAND ----------

# MAGIC %sql
# MAGIC describe database default

# COMMAND ----------

# DBTITLE 1,Criando um Database
# MAGIC %sql
# MAGIC create database db_daniel
# MAGIC Location "/FileStore/tables/daniel_pratica/DB"

# COMMAND ----------

# DBTITLE 1,Mostrando todos os databases
# MAGIC %sql
# MAGIC show databases

# COMMAND ----------

# DBTITLE 1,selecionando o Database desejado
# MAGIC %sql
# MAGIC use database db_daniel

# COMMAND ----------

# MAGIC %sql
# MAGIC select current_database()

# COMMAND ----------

# DBTITLE 1,Criando uma tabela no database desejado
# MAGIC %sql
# MAGIC create table db_daniel.teste (cod integer)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from teste

# COMMAND ----------

# MAGIC %sql
# MAGIC create table db_daniel.testado (cod integer)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from db_daniel.testado ;

# COMMAND ----------

# DBTITLE 1,Validando a criação das tabelas nas pastas
# MAGIC %fs ls "/FileStore/tables/daniel_pratica/DB/"

# COMMAND ----------

# DBTITLE 1,Criando outra Temp View
df.createOrReplaceTempView("v_order")

# COMMAND ----------

# MAGIC %sql 
# MAGIC select * from v_order

# COMMAND ----------

# DBTITLE 1,Transformando uma Temp View num dataframe novamente
df_orders = spark.table("v_order")
type(df_orders)

# COMMAND ----------

# DBTITLE 1,selecionar e Transformar uma Tabela de um database em Dataframe
df_teste = spark.table("db_daniel.testado")
display(df_teste)
