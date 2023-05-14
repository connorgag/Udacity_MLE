# General Health Predictions Based on Survey Data


This project predicts an individual's general health by using data that the individual provided. This survey was part of the Behavioral Risk Factor Surveillance System by the Center for Disease Control and Prevention. In this project, I create two models, one using AutoML with Azure ML and the other using HyperDrive, which is also part of Azure ML. As you will see, the AutoML did slightly better, but took much longer to run. I deploy the AutoML and test its REST endpoint.



## Project Set Up and Installation



1. The first step is to download the data from ttps://www.kaggle.com/datasets/cdc/behavioral-risk-factor-surveillance-system?datasetId=2192&sortBy=voteCount. 

If you want the best model possible, you can upload the data as is. If you are short on time (< 8 hours), you will need to take a sample of the data to upload to Azure ML. I took a sample of 150,000 of the ~ 450,000 rows. The computation time with this amount of data and the provied CPU still took around 7 hours. 


If you want to run the AutoML, you need to upload it to AzureML in the 'Data' section. Remember to remove the column '_RLHLTH' because this is a field derived from our target field. Call the data 'behavioral_data'. 

If you want to run Hyperdrive, you need to upload the data to the same directory as train.py. 


2. Next, connect the automl.ipynb and hypderdrive.ipynb jupyter notebooks to your Azure account. One easy way to do this is to upload this Project_Three folder into the 'Notebooks' section of Azure ML.  From either of these Jupyter notebooks, you can authenticate your account and begin running the cells. If you are running the notebooks outside the web UI (for example, in VS Code) you will need to download the config file first in order to authenticate. 
3. The next step is simply to run the cells in whichever notebook you choose. Hyperparameters can be changed or added in hyperdrive.ipynb and other configuration options can be changed in automl.ipynb. 
4. Deployment steps are in automl.ipynb. An endpoint can be created and called to using the cells toward the end of the notebook. 
5. Shut down any Webservices or compute clusters created by running the last cells in either notebook. 



## Dataset

### Overview

The dataset that I used is called Behavioral Risk Factor Surveillance System and was collected by the Center for Disease Control and Prevention. According to the dataset on Kaggle, "factors assessed by the BRFSS include tobacco use, health care coverage, HIV/AIDS knowledge or prevention, physical activity, and fruit and vegetable consumption. Data are collected from a random sample of adults (one per household) through a telephone survey." 

The file I will be using is from the survey taken in 2015, which includes 330 columns. 

More information on the data can be found on Kaggle at https://www.kaggle.com/datasets/cdc/behavioral-risk-factor-surveillance-system?datasetId=2192&sortBy=voteCount


After the initial experiment, I removed the feature '_RLHLTH' because it turned out to be a derived feature from the target outcome. 

### Task

The task is to predict an indvidual's general health score. This score (GENHLTH) is a self-reported general health score on a scale from 1 to 5, with 1 being the best and 5 being the worst. 

The features I will using are other self-reported factors such as diet, exercise, finances, etc. 


### Access

For AutoML:
I will access the data in the workspace by uploading it to the 'Data' section of Azure ML. I will then access the data from there using the python SDK. 


For HyperDrive:
The training script accesses the data from the same place, but it is important to replace the credentials in train.py with your own so that you can authenticate and access the data. 


## Automated ML

The target that I want to predict is GENHLTH, which is a continuous variable. This variable ranges from 1 to 5, with 1 meaning the individual has reported that they are in very good health and 5 is reported bad general health. 

```
automl_settings = {
    "experiment_timeout_hours": 1,
    "max_concurrent_iterations": 4,
    "primary_metric" : 'normalized_root_mean_squared_error'
}

automl_config = AutoMLConfig(compute_target=compute_target,
                             task = "regression",
                             training_data=dataset,
                             label_column_name="GENHLTH",   
                             path = '.',
                             enable_early_stopping= True,
                             featurization= 'auto',
                             debug_log = "automl_errors.log",
                             **automl_settings
                            )
```

My AutoML settings define the regression problem with the target of GENHLTH. I increased the experiment timeout hours to be 1 hour because the dataset is quite large. I chose normalized root mean squared error because it is common metric for regression problems and will allow me to compare this model with the HyperDrive one. 


### Results
*TODO*: What are the results you got with your automated ML model? What were the parameters of the model? How could you have improved it?

*TODO* Remember to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

The best model had a normalized root mean squared error of about .101, which used Stack Ensemble. This algorithm uses the output of many other algorithms in it's calculation. The main way I could improve this model is to use all of the data, instead of just taking a sample. I would need my own Azure account to do this because it would take so long. 
![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Three/Screenshots/Automl_run_details.png?raw=true)



![alt text](https://github.com/connorgag/Udacity_MLE/blob/main/Project_Three/Screenshots/AutoML_best_run.png?raw=true)



## Hyperparameter Tuning

I used a neural network regression model using the MLPRegressor class. I chose a neural network because they are typically good at understanding complex relationships within the data. The dataset I chose has many columns, so a neural network made sense because it could easily work with the large number of features. Another reason I chose it was because it is easy to tune the hyperparameters in a neural network. 

The hyperparameters that I chose include the maximum iterations and the activation function. 

I used the stochastic solver 'adam', so the maximum iterations that I chose determined the number of epochs if the model does not converge. I set the options for this to be between 200 and 3000, stepping by 100. 

I also set options for the activation function to be used in the hidden layer. The options that were available in this case were identity, logistic, relu, and tanh. 


### Results
*TODO*: What are the results you got with your model? What were the parameters of the model? How could you have improved it?

*TODO* Remember to provide screenshots of the `RunDetails` widget as well as a screenshot of the best model trained with it's parameters.

## Model Deployment

I registered both models, but only deployed the AutoML model. This is done with the python sdk, but can also be accomplished with the AzureML UI. 


You will need to prepare the input data in json format, put your credentials in a header dictionary, and find the scoring url associated with the model. 

Here you'll create your request by feeding in the required parameters. 

```
req = urllib.request.Request(url, body, headers)
```

You'll then use urllib to open the request, which will prompt a response. This response can be seen by calling response.read(). 

Any errors that are raised with this call will be caught and displayed by the exception. 

```
try:
    response = urllib.request.urlopen(req)
    print(response.read())
except urllib.error.HTTPError as error:
    print("Request failed with status code: " + str(error.code))
```

This is a brief overview, for more detail into how to query the endpoint, go to automl.ipynb towards the end of the file. 


## Screen Recording

https://youtu.be/CUV1OO85_BU
