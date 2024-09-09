# Databricks notebook source
# Create a Spark DataFrame with specified values
values = [("what is the capital of France?",), ("what is the best dishwasher brand?",)]
df = spark.createDataFrame(values, ["value"])
display(df)

# COMMAND ----------

spark.sql("use catalog mgiglia")

# COMMAND ----------

spark.sql("use schema adventure")

# COMMAND ----------

df.createOrReplaceTempView("text_data")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from text_data;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   value
# MAGIC   ,ai_query(
# MAGIC     'mg-completions'
# MAGIC     ,request => '{
# MAGIC       "messages":[{"role":"user","content":' || value ||'}]
# MAGIC       ,"max_tokens":128
# MAGIC     }' 
# MAGIC     -- ,returnType => <Please provide your endpoint return type here!>
# MAGIC   ) as response
# MAGIC FROM 
# MAGIC   text_data

# COMMAND ----------

# MAGIC %md
# MAGIC ***

# COMMAND ----------

df = spark.table("mgiglia.adventure.installs")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION mgiglia.adventure.tToSparkSQL_identifyCommands(text STRING)
# MAGIC   RETURNS STRING
# MAGIC   RETURN ai_query(
# MAGIC     'mg-completions',
# MAGIC     request => '{
# MAGIC       "messages":[{"role":"user","content": You are a programmer reviewing the following t-sql: ' || text ||' .  Please wrap each command with a command_start and command_end comment.}]
# MAGIC       ,"max_tokens": 30000
# MAGIC     }')
# MAGIC ;

# COMMAND ----------

from pyspark.sql.functions import explode, split, col

# COMMAND ----------

df_exploded = df.withColumn("value", explode(split(col("value"), "GO")))

df_exploded.write.mode("overwrite").saveAsTable("mgiglia.adventure.installs_exploded")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select * from exploded_text_data LIMIT 100;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE OR REPLACE TABLE mgiglia.adventure.install_commands AS 
# MAGIC SELECT
# MAGIC   *
# MAGIC   ,mgiglia.adventure.tToSparkSQL_identifyCommands(value) as wrapped_commands
# MAGIC FROM mgiglia.adventure.installs;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT * from mgiglia.adventure.test;
