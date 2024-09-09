# Databricks notebook source
import mlflow.deployments

client = mlflow.deployments.get_deploy_client("databricks")

completions_response = client.predict(
    endpoint="mg-completions",
    inputs={
        "prompt": "What is the capital of France?",
        "temperature": 0.1,
        "max_tokens": 10,
        "n": 2
    }
)

# Print the response
print(completions_response)

# COMMAND ----------

chat_response
