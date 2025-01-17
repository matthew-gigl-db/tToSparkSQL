# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC # Install Adventure Works
# MAGIC
# MAGIC ***
# MAGIC
# MAGIC The purpose of this notebook is to create the catalog, schema and volumes that we'll use as a proxy to a replicated SQL Server Database that T-SQL reports were written against.  The SQL Server Database used is the famous "Adventure Works" that is still used today for training and certification exams for SQL Server and PowerBI.  
# MAGIC
# MAGIC The files used are the 2022 version of the Adventure Works database, retrieved from the official Microsoft SQL Server Samples [GitHub](https://github.com/microsoft/sql-server-samples) on September 5, 2024.  
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Notebook Set Up
# MAGIC ***

# COMMAND ----------

# DBTITLE 1,Upgrading the Databricks SDK with Pip Command
# MAGIC %pip install databricks-sdk --upgrade

# COMMAND ----------

# DBTITLE 1,Restarting Python Runtime in Databricks
dbutils.library.restartPython()

# COMMAND ----------

# DBTITLE 1,Set Databricks Widget Notebook Parameter Inputs
dbutils.widgets.text("bundle.workspace.file_path", "..")
dbutils.widgets.text("bundle.catalog", "main")

# COMMAND ----------

# DBTITLE 1,Retrieve Widget Inputs
workspace_file_path = dbutils.widgets.get("bundle.workspace.file_path")
catalog_use = dbutils.widgets.get("bundle.catalog")

# COMMAND ----------

# DBTITLE 1,Set Absolute Paths for Project Source Files and Bundle Fixtures
import os

src_path = os.path.abspath(f"{workspace_file_path}/src")
fixtures_path = os.path.abspath(f"{workspace_file_path}/fixtures")

print(f"""
  src_path = {src_path}
  fixtures_path = {fixtures_path}
""")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Catalog, Schema & Volume Creation 
# MAGIC ***

# COMMAND ----------

# DBTITLE 1,Set Catalog
# MAGIC %sql
# MAGIC
# MAGIC DECLARE OR REPLACE VARIABLE new_catalog STRING;
# MAGIC SET VAR new_catalog = :`bundle.catalog`;
# MAGIC SELECT new_catalog; 

# COMMAND ----------

# DBTITLE 1,Create the Catalog If Not Exists
# MAGIC %sql
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create catalog if not exists new_catalog;" 

# COMMAND ----------

# DBTITLE 1,Create the Schema If Not Exists
# MAGIC %sql 
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create schema if not exists IDENTIFIER(new_catalog || '.adventure');"  

# COMMAND ----------

# DBTITLE 1,Create Volume If Not Exists
# MAGIC %sql
# MAGIC
# MAGIC EXECUTE IMMEDIATE "create volume if not exists IDENTIFIER(new_catalog || '.adventure' || '.landing')"

# COMMAND ----------

# DBTITLE 1,Set Volume Path
volume_path = f"/Volumes/{catalog_use}/adventure/landing"
volume_path

# COMMAND ----------

# MAGIC %md
# MAGIC ### Copy CSV Files from the Workspace to the Volume 
# MAGIC ***

# COMMAND ----------

# DBTITLE 1,Initialize the Workspace Client
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# COMMAND ----------

# DBTITLE 1,Retrieve File Details from the fixtures Workspace Directory
adventure_files = w.workspace.list(f"{fixtures_path}", recursive=True)
adventure_files = [file.as_dict() for file in adventure_files]

# COMMAND ----------

# DBTITLE 1,Display the file details
display(adventure_files)

# COMMAND ----------

# DBTITLE 1,List the file paths Adventure Works OLTP and DW Data Files
file_paths = [file["path"] for file in adventure_files if file["object_type"] == "FILE" and ".git" not in file["path"]]
file_paths

# COMMAND ----------

# DBTITLE 1,Create Volume Sub Directories for Data Files and t-SQL Files
new_dirs = [f"{volume_path}/data/dw", f"{volume_path}/data/oltp", f"{volume_path}/t-sql/installs", f"{volume_path}/t-sql/reports"]

for dir in new_dirs:
  dbutils.fs.mkdirs(dir)

display(
  dbutils.fs.ls(f"{volume_path}/data") + dbutils.fs.ls(f"{volume_path}/t-sql")
)

# COMMAND ----------

# DBTITLE 1,Copy files from the Workspace to the Volume
import shutil

for file_path in file_paths:
    file_name = file_path.split("/")[-1]
    if "adventure-works-oltp" in file_path:
        destination_path = f"{volume_path}/data/oltp/{file_name}"
    elif "adventure-works-dw" in file_path:
        destination_path = f"{volume_path}/data/dw/{file_name}"
    elif "t-sql/installs" in file_path:
        destination_path = f"{volume_path}/t-sql/installs/{file_name}"
    elif "t-sql/reports" in file_path:
        destination_path = f"{volume_path}/t-sql/reports/{file_name}"
    else:
        destination_path = f"{volume_path}/data/{file_name}"
    shutil.copy(file_path, destination_path)

# COMMAND ----------

# DBTITLE 1,Show Files in Volume
display(
  dbutils.fs.ls(f"{volume_path}/data") +
  dbutils.fs.ls(f"{volume_path}/data/dw") + 
  dbutils.fs.ls(f"{volume_path}/data/oltp") + 
  dbutils.fs.ls(f"{volume_path}/t-sql") +
  dbutils.fs.ls(f"{volume_path}/t-sql/installs") +
  dbutils.fs.ls(f"{volume_path}/t-sql/reports")
)

# COMMAND ----------

# MAGIC %md
# MAGIC *** 
# MAGIC
# MAGIC ### Not Run:

# COMMAND ----------

# DBTITLE 1,Drop Volume - Development Only
# MAGIC %sql
# MAGIC
# MAGIC -- EXECUTE IMMEDIATE "drop volume if exists IDENTIFIER(new_catalog || '.adventure' || '.landing')"

# COMMAND ----------

# MAGIC %md
# MAGIC ***
