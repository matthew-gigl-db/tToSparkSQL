# Databricks notebook source
# MAGIC %sql
# MAGIC
# MAGIC DECLARE OR REPLACE VARIABLE new_catalog STRING;
# MAGIC SET VAR new_catalog = :`bundle.catalog`;
# MAGIC SELECT new_catalog; 

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create catalog if not exists new_catalog;" 

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create schema if not exists IDENTIFIER(new_catalog || '.adventure');"  

# COMMAND ----------

1+1

# COMMAND ----------

2+2
