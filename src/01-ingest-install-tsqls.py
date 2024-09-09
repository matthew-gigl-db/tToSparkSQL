# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest T-SQL Install Files as Data
# MAGIC
# MAGIC The purpose of this notebook is to ingest the OLTP and DW T-SQL install files from the project's *fixtures* folder as data files that we can parse and send to an LLM later for conversion to Spark SQL.  
# MAGIC
# MAGIC Note: once DBSQL Warehouses are upgraded to 15.4 LTS or above, this notebook may be run against a Serverless SQL endpoint.
# MAGIC
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC ## Notebook Setup 
# MAGIC ***

# COMMAND ----------

# MAGIC %md
# MAGIC ### Set Notebook Parameters

# COMMAND ----------

dbutils.widgets.text("bundle.catalog", "main")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DECLARE OR REPLACE VARIABLE catalog_use STRING;
# MAGIC SET VAR catalog_use = :`bundle.catalog`;
# MAGIC SELECT catalog_use; 

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest the SQL Files as Variant 
# MAGIC ***

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC DECLARE OR REPLACE VARIABLE sql_stmnt STRING;
# MAGIC SET VAR sql_stmnt = "
# MAGIC   CREATE OR REPLACE TABLE IDENTIFIER(catalog_use || '.adventure.installs') AS 
# MAGIC   SELECT
# MAGIC      _metadata.file_modification_time as file_modification_time
# MAGIC     ,_metadata.file_block_length as file_block_length
# MAGIC     ,_metadata.file_name as file_name
# MAGIC     ,_metadata.file_size as file_size
# MAGIC     ,_metadata.file_block_start as file_block_start
# MAGIC     ,_metadata.file_path as file_path
# MAGIC     ,_metadata as metadata
# MAGIC     ,*
# MAGIC   FROM 
# MAGIC     read_files(
# MAGIC       '/Volumes/' || catalog_use || '/adventure/landing/t-sql/installs/'
# MAGIC       ,format => 'text'
# MAGIC       ,wholeText => 'true'
# MAGIC     )
# MAGIC ";
# MAGIC
# MAGIC EXECUTE IMMEDIATE sql_stmnt;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SHOW CREATE TABLE IDENTIFIER(catalog_use || '.adventure.installs');

# COMMAND ----------

# MAGIC %md
# MAGIC ***
