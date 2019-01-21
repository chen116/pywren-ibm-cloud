
# coding: utf-8

# # <span style="color:blue">Stock prediction with Monte Carlo methods</span>
# We demonstrate how to run Monte Carlo simuluations with [PyWren-IBM-Cloud](https://github.com/pywren/pywren-ibm-cloud) over IBM Cloud Functions. This notebook contains an example of stock prediction with Monte Carlo. The goal of this notebook is to demonstrate how IBM Cloud Functions can benefit Monte Carlo simulations and not how stock prediction works. As stock prediction is very complicated and requires many prior knowledge and correct models, we did not innovate the Monte Carlo Method for handling the unpredictability of stock prices, nor do we provide any results for prediction based on long term data sources.
# 
# Requirements to run this notebook:
# 
#     * IBM Cloud account. 
#       Register to IBM Cloud Functions, IBM Cloud Object Storage (COS), Watson Studio
#     * You will need to have at least one existing object storage bucket. Follow COS UI to create a bucket if needed 
#     * IBM Watson Studio Python notebook

# ## <span style="color:blue">Step 1  - Install dependencies </span>
# 
# Install dependencies

# In[ ]:


import numpy as np
from time import time
import matplotlib.pyplot as plt
import scipy.stats as scpy
import logging

# This script installs PyWren-IBM-Cloud from https://github.com/pywren/pywren-ibm-cloud
# get_ipython().system('curl -fsSL "https://git.io/fhe9X" | sh')
# try:
import pywren_ibm_cloud as pywren
# except:
    # get_ipython().system('curl -fsSL "https://git.io/fhe9X" | sh')
    # import pywren_ibm_cloud as pywren

# you can modify logging level if needed
logging.basicConfig(level=logging.DEBUG)


# ## <span style="color:blue">Step 2 - Write Python code that implements Monte Carlo simulation </span>
# Below is an example of Python code to demonstrate Monte Carlo model for stock prediction.
# 
# 'StockData' is a  Python class that we use to represent a single stock. 
#  You may configure the following parameters:
# 
#     MAP_INSTANCES - number of IBM Cloud Function invocations. Default is 1000
#     forecasts_per_map - number of forecasts to run in a single invocation. Default is 100
#     day2predict - number of days to predict for each forecast. Default is 730 days
# 
# Our code contains two major Python methods:
# 
#     def process_forecasts(data=None) - a function to process number of forecasts and
#       days as configured. (aka "map" in map-reduce paradigm)
#     def combine_forecasts(results) - summarize results of all process_forecasts
#       executions (aka "reduce" in map-reduce paradigm)
#     
#     

# In[ ]:


MAP_INSTANCES = 10

class StockData:
    forecasts_per_map = 100
    days2predict = 730

    def __init__(self, title, drift, std_dev, last_value):
        self.title = title
        self.last_value = last_value
        self.std_dev = std_dev
        self.drift = drift

    def single_forecast_generator(self):
        predicts_est = [self.last_value]
        for predict in range(1, self.days2predict + 1):
            rand = np.random.rand()
            pow_r = scpy.norm.ppf(rand)
            predicts_est.append(predicts_est[predict - 1] * np.exp(self.drift + (self.std_dev * pow_r)))
        return predicts_est

def process_forecasts(data=None):
    end = current_stock.days2predict
    mid = int(end / 2)
    hist_end = list()
    hist_mid = list()
    for i in range(StockData.forecasts_per_map):
        frc = current_stock.single_forecast_generator()
        hist_end.append(frc[end])
        hist_mid.append(frc[mid])
    return hist_mid, hist_end


def combine_forecasts(results):
    print(np.__version__)  # in order to import numpy
    hist_end = list()
    hist_mid = list()
    for single_map_result in results:
        hist_end.extend(single_map_result[1])
        hist_mid.extend(single_map_result[0])
    return {"futures": None, "results": (hist_mid, hist_end)}


# ## <span style="color:blue">Step 3 - Configure access to your COS account and Cloud Functions</span>
# 
# Configure access details to your IBM COS and IBM Cloud Functions.  'storage_bucket'  should point to some pre-existing COS bucket. This bucket will be used by PyWren to store intermediate results. All results will be stored in the folder `Pywren.jobs`. For additional configuration parameters see [configuration section](https://github.com/pywren/pywren-ibm-cloud)

# In[ ]:


config = {
          'ibm_cf':  {'endpoint': '<IBM Cloud Functions Endpoint>', 
                      'namespace': '<NAMESPACE>', 
                      'api_key': '<API KEY>'}, 
          'ibm_cos': {'endpoint': '<IBM Cloud Object Storage Endpoint>', 
                      'api_key' : '<API KEY>'},
           'pywren' : {'storage_bucket' : '<IBM COS BUCKET>'}}


# ## <span style="color:blue">Step 4 - Input data on the past stock prices </span>
# This step is mandatory to run our example. The raw stock daily data need to be prepared prior used by the code.
# You can follow the next steps to create different input data. You may use any spreadsheet for this process or any other tool.
# 
#     * Fetch historical daily value of the stock from some reliable finance website
#     * Calculate ln() function of two consecutive days ln (today price / yesterday price )
#     * Calculate the variance 'var', the average 'u' and standard deviation of the previous results
#     * Calculate the drift by equation drift = u - (var^2 / 2 )

# In[ ]:


total_forecasts = MAP_INSTANCES * StockData.forecasts_per_map

current_stock = StockData(title="Example 2014, 2015, 2016", drift=-0.00022513546014255100, std_dev=0.0121678341323272,
                               last_value=159.44)
print("Current Stock: " + current_stock.title)
print("Total Forecasts: " + str(total_forecasts))
print("Days to Predict: " + str(current_stock.days2predict))


# ## <span style="color:blue">Step 5 - Deloy of PyWren runtime</span>
# 
# The following will create an action "pywren_3.5" in your Cloud Function account. This action contains runtime of the PyWren needed to execute your code. Alternative you may create a runtime with manual steps as described [here](https://github.com/pywren/pywren-ibm-cloud/tree/master/runtime)

# In[ ]:


# from pywren_ibm_cloud.deployutil import clone_runtime
# clone_runtime('ibmfunctions/pywren:3.5', config, 'pywren-ibm-cloud')


# ## <span style="color:blue"> Step 6 - Execute simulation with PyWren over IBM Cloud Functions </span>

# In[ ]:


iterdata = [{}] * MAP_INSTANCES
start_time = time()
print ("Monte Carlo simulation for {} using {} forecasts spawing over {} IBM Cloud Function invocations".format(current_stock.title, total_forecasts, MAP_INSTANCES))
# obtain PyWren-IBM-Cloud executor
# pw = pywren.ibm_cf_executor(config=config, runtime='pywren_3.5')
pw = pywren.ibm_cf_executor()
# execute the code
pw.map_reduce(process_forecasts, iterdata, combine_forecasts, reducer_wait_local=False, remote_invocation=True)
#get results
result_object = pw.get_result()
result_obj = result_object["results"]

elapsed = time()
print("\nCompleted in: " + str(elapsed - start_time) + " seconds")


# ## <span style="color:blue">Step 7 - Print the graphs </span>

# In[ ]:


'''Histogram for end prediction forecast plot'''

end_data = result_obj[1]
print("END Histogram for {} based on {} forecasts. Predicted price after {} days".format(current_stock.title,total_forecasts, current_stock.days2predict ))
plt.hist(end_data, bins='auto')
plt.grid(True)
plt.title("End prediction period histogram")
plt.ylabel("Number of forecasts to predict the price")
plt.xlabel("Stock price in US Dollars")
plt.show()

