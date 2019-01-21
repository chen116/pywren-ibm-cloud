
# coding: utf-8

# # π Estimation with Monte Carlo methods
# We demonstrate how to run Monte Carlo simulations with PyWren-IBM-Cloud over IBM Cloud Functions. This notebook contains an example of estimation the number π with Monte Carlo. The goal of this notebook is to demonstrate how IBM Cloud Functions can benefit Monte Carlo simulations and not how it can be done using PyWren-IBM-Cloud.<br>
# A Monte Carlo algorithm would randomly place points in the square and use the percentage of randomized points inside of the circle to estimate the value of π
# ![pi](https://upload.wikimedia.org/wikipedia/commons/8/84/Pi_30K.gif)
# Requirements to run this notebook:
# 
# * IBM Cloud account. 
#   Register to IBM Cloud Functions, IBM Cloud Object Storage (COS), Watson Studio
# * You will need to have at least one existing object storage bucket. Follow COS UI to create a bucket if needed 
# * IBM Watson Studio Python notebook

# # Step 1 - Install dependencies
# Install dependencies

# In[ ]:


from time import time
from random import random
import logging

# This script installs PyWren-IBM-Cloud from https://github.com/pywren/pywren-ibm-cloud
# get_ipython().system('curl -fsSL "https://git.io/fhe9X" | sh')
# try:
#     import pywren_ibm_cloud as pywren
# except:
#     get_ipython().system('curl -fsSL "https://git.io/fhe9X" | sh')
#     import pywren_ibm_cloud as pywren

# you can modify logging level if needed
logging.basicConfig(level=logging.INFO)


# # Step 2 - Write Python code that implements Monte Carlo simulation 
# Below is an example of Python code to demonstrate Monte Carlo model for estimate PI
# 
# 'EstimatePI' is a Python class that we use to represent a single PI estimation. You may configure the following parameters:
# 
# MAP_INSTANCES - number of IBM Cloud Function invocations. Default is 100<br>
# randomize_per_map - number of points to random in a single invocation. Default is 10,000,000
# 
# Our code contains two major Python methods:
# 
# def randomize_points(self,data=None) - a function to random number of points and return the percentage of points
#     that inside the circle<br>
# def process_in_circle_points(self, results, futures): - summarize results of all randomize_points
#   executions (aka "reduce" in map-reduce paradigm)

# In[ ]:


MAP_INSTANCES = 100


class EstimatePI:
    randomize_per_map = 10000000

    def __init__(self):
        self.total_randomize_points = MAP_INSTANCES * self.randomize_per_map

    def __str__(self):
        return "Total Randomize Points: {:,}".format(self.randomize_per_map * MAP_INSTANCES)

    @staticmethod
    def predicate():
        x = random()
        y = random()
        return (x ** 2) + (y ** 2) <= 1

    def randomize_points(self, data):
        in_circle = 0
        for _ in range(self.randomize_per_map):
            in_circle += self.predicate()
        return float(in_circle / self.randomize_per_map)

    def process_in_circle_points(self, results, futures):
        in_circle_percent = 0
        for map_result in results:
            in_circle_percent += map_result
        run_statuses = [f.run_status for f in futures]
        invoke_statuses = [f.invoke_status for f in futures]
        estimate_PI = float(4 * (in_circle_percent / MAP_INSTANCES))
        return {"run_statuses": run_statuses, "invoke_statuses": invoke_statuses, "results": estimate_PI}


# # Step 3 - Configure access to your COS account and Cloud Functions
# Configure access details to your IBM COS and IBM Cloud Functions. 'storage_bucket' should point to some pre-existing COS bucket. This bucket will be used by PyWren to store intermediate results. All results will be stored in the folder Pywren.jobs. For additional configuration parameters see configuration section

# In[ ]:


config = {'ibm_cf':  {'endpoint': '<IBM Cloud Functions Endpoint>', 
                      'namespace': '<NAMESPACE>', 
                      'api_key': '<API KEY>'}, 
          'ibm_cos': {'endpoint': '<IBM Cloud Object Storage Endpoint>', 
                      'api_key' : '<API KEY>'},
           'pywren' : {'storage_bucket' : '<IBM COS BUCKET>'}}


# # Step 4 - Deloy of PyWren runtime
# The following will create an action "pywren_3.5" in your Cloud Function account. This action contains runtime of the PyWren needed to execute your code. Alternative you may create a runtime with manual steps as described here

# In[ ]:


# from pywren_ibm_cloud.deployutil import clone_runtime
# clone_runtime('ibmfunctions/pywren:3.5', config, 'pywren-ibm-cloud')


# # Step 5 - Execute simulation with PyWren over IBM Cloud Functions 

# In[ ]:


iterdata = [0] * MAP_INSTANCES
est_pi = EstimatePI()

start_time = time()
print("Monte Carlo simulation for estimating PI spawing over {} IBM Cloud Function invocations".format(MAP_INSTANCES))
# obtain PyWren-IBM-Cloud executor
# pw = pywren.ibm_cf_executor(config=config, runtime='pywren_3.5')
pw = pywren.ibm_cf_executor()
# execute the code
pw.map_reduce(est_pi.randomize_points, iterdata, est_pi.process_in_circle_points, reducer_wait_local=False, remote_invocation=True)
#get results
result_object = pw.get_result()
result_obj = result_object["results"]
elapsed = time()
print(str(est_pi))
print("Estimation of Pi: ", result_obj)
print("\nCompleted in: " + str(elapsed - start_time) + " seconds")

