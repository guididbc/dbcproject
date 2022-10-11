# Databricks notebook source
from pyspark.sql.functions import *
def add_date_process(df_input):
    df_output = df_input.withColumn("date_process", current_timestamp())
    return df_output

# COMMAND ----------

def add_id (df_input):
    df_output = df_input.withColumn("id", monotonically_increasing_id()+1)
    return df_output
