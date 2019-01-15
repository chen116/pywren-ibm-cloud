"""
Simple PyWren example using one single function invocation
"""
import pywren_ibm_cloud as pywren



my_source = my_source(socket,window=5)
my_sink = my_sink(sth)

def my_func(x):
	return sum(x)
pw = pywren.ibm_cf_executor()
pw.streamprocess(my_func,my_sink)







def my_function(x):
    return x + 7

if __name__ == '__main__':
    pw = pywren.ibm_cf_executor()
    print(pw.executor.invoker.client.is_cf_cluster)
    pw.call_async(my_function, 3)
    print (pw.get_result())
