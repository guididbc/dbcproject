# Databricks notebook source
# MAGIC %fs ls dbfs:/FileStore/tables/pratica

# COMMAND ----------

# DBTITLE 1,Bibliotecas
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, IntegerType ## seleciona algumas bibliotecas de Types
from pyspark.sql.types import * ## seleciona todas as bibliotecas de Types
import pandas as pd

# COMMAND ----------

# DBTITLE 1,Variáveis de arquivos
caminho_cust = '/FileStore/tables/pratica/olist_customers_dataset.csv'

# COMMAND ----------

type(caminho_cust)

# COMMAND ----------

# DBTITLE 1,Importando arquivos
df = spark.read.format("csv")\
.option("inferSchema", True)\
.option("header", True)\
.option("delimiter", ",")\
.load(caminho_cust)

# COMMAND ----------

type(df)

# COMMAND ----------

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

# DBTITLE 1,Cria um dataframe de esquema para utilizar no df principal e alterar o esquema original
df_schema = StructType([
    StructField("customer_id", StringType()),
    StructField("customer_unique_id", StringType()),
    StructField("customer_zip_code_prefix", StringType()),
    StructField("customer_city", StringType()),
    StructField("customer_state", StringType())
    
])

# COMMAND ----------

type(df_schema)

# COMMAND ----------

# DBTITLE 1,Importando arquivo com alteração do esquema
df = spark.read.format("csv")\
.schema(df_schema)\
.option("header", True)\
.option("delimiter", ",")\
.load(caminho_cust)

# COMMAND ----------

df.toPandas()

# COMMAND ----------


