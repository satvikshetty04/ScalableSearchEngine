## Team Members
* Amit Kanwar (akanwar2@ncsu.edu)
* Ashis Sahoo (aksahoo@ncsu.edu)
* Satvik Shetty (smshetty@ncsu.edu)

## Description

To create a Data Intensive application that can handle high velocity/volume. The application
will consist of a machine learning model that performs following tasks:
* Updates Model in real-time based on input data.
* Serves user CRUD operations in real-time.

## Claims

We aim to build a high velocity/high volume system that:
* Will handle CRUD and search operations on a large volume of data (around 2-3 TB).
* Will have the same performance irrespective of the velocity of the incoming data, without
any loss of information.
* Has constant Latency and Throughput with increase in data volume and number of
CRUD and search operations on the dataset.
* Application is accessible even if one of the worker nodes fails in the system.
