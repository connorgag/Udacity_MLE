# Project 2: Operationalizing Machine Learning

By Connor Gag

## Overview
In this project, I demonstrated my ability to deploy many parts of a machine learning pipeline in Azure ML. I created each of these parts by using the Azure UI as well as by using the Python SDK. These steps include creating the AutoML, deploying it, and understanding and consuming the endpoint. I consumed the model using a REST endpoint and created a pipeline to automate the workflow. 

## Architectural Diagram
![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Architectural%20Diagram_%20Operationalizing%20Machine%20Learning%20.jpg?raw=true)

## Key Steps
1. Upload Bank Marketing dataset

Here we uploaded the bank marketing dataset. With Azure you can view the features and their types before adding it, as well as choosing other configurations for the data. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/bank_dataset_screenshot.png?raw=true)




2. Run the dataset through AutoML
   
Here is our AutoML result under the "Jobs" section. You can see that it took about 20 minutes to run. Before running this we created a compute cluster called "project-2-compute". AutoML is important because it tests out many algorithms on our data and ranks them all based on the primary metric that we decide. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Completed_Screenshot.png?raw=true)




3. Choose the best option

Now that we have run our dataset through the AutoML supplied by Azure, we can now view the results. In our case, we chose our primary metric as AUC weighted, so I ranked the algorithms based on this. Then, I chose the top one, which had an AUC Weighted about about .95. We will work with this algorithm in the next steps. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Best_Model_Screenshot.png?raw=true)




4. Deploy the best option and enable application insights, then view the logs

I deployed the model from the last step. Once this deployed endpoint was healthy, I created and ran enable_app_insights.py, which enabled the application insights. This allows us to monitor our model closely. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/App_Insights_Screenshot.png?raw=true)


Running log.py gives us log output from our deployed model, allowing us to monitor our model. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/logs_py_output_screenshot.png?raw=true)




5. Understand API Endpoint using Swagger

Here I downloaded the Swagger json file from the model deployment section of Azure ML. Then I started a python server on port 8000 and opened it to view the API specifications. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Swagger_Screenshot.png?raw=true)


Going into a little more detail, here we can see the specific HTTP requests that are allowed by the API. We can even view the formatting for our requests by looking at the example input and output payloads. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Swagger_Screenshot_2.png?raw=true)




6. Set Benchmarks 

We are running benchmark.sh, which tells us how our endpoint is doing when it comes to responding to our requests. This is important so that we have a benchmark that will help us detect anomalies in the future. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Benchmark_Screenshot_1.png?raw=true)


Going deeper into our results, we can view the time it took for the connections, the number of successful requests, the time per request, etc. For example, here each request took 414 milliseconds. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Benchmark_Screenshot_2.png?raw=true)




7. Create Pipeline using Python SDK

This is where we created the pipeline using the Python SDK. Using RunDetails shows us the status of the run and the time it took to finish. It also shows us a diagram of the completed pipeline. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/RunDetails_Screenshot.png?raw=true)


We can view our available pipelines in the "Pipeline" section of Azure ML. We will continue this demo using the top one, entitled "icy_shark_n8d9vm2x". 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Pipeline_Section_Screenshot.png?raw=true)


This is a completed view of our pipeline under "Jobs". As you can see, it completed successfully. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Completed_Pipeline_Screenshot.png?raw=true)


This is ML studio showing the pipeline endpoint as Active. Under the "Pipelines" section, we can look at the "Published Pipelines Overview" to see that the pipeline has a status of Active and has an available REST endpoint, which we will use to consume the model. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Published_Pipeline_Overview_Screenshot.png?raw=true)


Looking into this pipeline run further, we can view all of the steps. In this case there are two steps: One to upload the bank marketing dataset and one to run it through our chosen AutoML model. It is important to be able to view the pipeline so that we can understand it and make changes in the future. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Bank_and_AutoML_Screenshot.png?raw=true)




8. Schedule the Run

Under "Jobs", we can schedule the pipeline to run at whatever pattern we like. I arbitrarily chose every Monday through Friday at 10:00 PM (UTC), but you can change this based on your own situation and needs. This automation is helpful because it takes out the manual work associated with running a pipeline. 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/Scheduled_Run_Screenshot.png?raw=true)


9. Consume Endpoints

Here I ran endpoint.py and received the JSON payload as output. We can interpret this by saying that the first example we gave has a predicted value of "yes" and the second example we gave has a predicted value of "no". 

![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Two/Screenshots/endpoint_output.png?raw=true)




## Screen Recording
https://youtu.be/mNSjadBRQUM

## Future Improvements
There are many things you could do to improve this project. For example, you could switch from AutoML to Hyperdrive and do some hyperparameter tuning, which may result in a better model if you have a good understanding of the domain. Another option would be to collect more data, which may make future predictions more accurate. 