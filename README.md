# pinterest-data-pipeline841

## Table of contents

- [Project Description](#project-description)
- [Project Installation and Dependencies](#project-installation-and-dependencies)
- [The Data](#the-data)
- [Tools used](#tools-used)
- [Architecture Overview](architecture-overview)
Building the pipeline
Create an Apache cluster using AWS MSK
Create a client machine for the cluster
Enable client machine to connect to the cluster
Install Kafka on the client machine
Create topics on the Kafka cluster
Delivering messages to the Kafka cluster
AWS API Gateway
Sending messages to the cluster using the API gateway
Connecting the Apache cluster to AWS S3 bucket
Batch processing data using Apache Spark on Databricks
Clean data using Apache Spark on Databricks
Querying the data using Apache Spark on Databricks
Orchestrating automated workflow of notebook on Databricks
Processing streaming data
Create data streams on Kinesis
Create API proxy for uploading data to streams
Sending data to the Kinesis streams
Processing the streaming data in Databricks
Next steps

## Project Description

This project emulates a Pinterest-like data pipeline to handle real-time user-generated data. The aim is to simulate the process of ingesting, processing, and storing data at scale, using AWS services and Kafka. There are two pipelines built in the project ; 
I. Computing real-time metrics (such as profile popularity, which would be used to recommend that profile in real-time)
II. Computing metrics that depend on historical data (such as the most popular category this year) 
I've learned about the complexities of managing data pipelines in a cloud environment, the importance of data stream partitioning for scalability and fault tolerance, and the intricacies of configuring AWS services and Kafka for real-time data processing. Alongside this technical side, I learned how important adjust the cost. So the architecture should be designed with a focus on scalability and fault tolerance, employing data stream partitioning and optimized resource allocation to efficiently manage data flow and processing tasks. This approach ensured that the system could handle varying data volumes effectively, minimizing costs while maximizing performance.


## Project Installation and Dependencies

The modules need to be installed:

- `python-dotenv`
- `sqlalchemy`
- `requests`

For the Virtual environment; I used the CONDA environment

- Create a Conda environment 
`conda create -n your_env_name python=3.x`
`conda activate your_env_name`
`pip install -r requirements.txt`

## The Data

To emulate the kind of data that Pinterest's engineers are likely to work with, this project contains a script, [user_posting_emulation.py] that when run from the terminal mimics the stream of random data points received by the Pinterest API when POST requests are made by users uploading data to Pinterest.

Running the script instantiates a database connector class, which is used to connect to an AWS RDS database containing the following tables:

- `pinterest_data` contains data about posts being updated to Pinterest
- `geolocation_data` contains data about the geolocation of each Pinterest post found in pinterest_data
- `user_data` contains data about the user that has uploaded each post found in pinterest_data
  
The `run_infinite_post_data_loop()` method infinitely iterates at random intervals between 0 and 2 seconds, selecting all columns of a random row from each of the three tables and writing the data to a dictionary. The three dictionaries are then printed to the console.

Examples of the data generated look like the following:

Examples of the data generated look like the following:

pinterest_data:
```
{
  "index": 5730,
  "unique_id": "1e1f0c8b-9fcf-460b-9154-c775827206eb",
  "title": "Island Oasis Coupon Organizer",
  "description": "Description Coupon Organizer in a fun colorful fabric -island oasis, Great Size for the 'basic' couponer - holds up to 500 coupons with ease, and is made long enough so that you…",
  "poster_name": "Consuelo Aguirre",
  "follower_count": "0",
  "tag_list": "Grocery Items,Grocery Coupons,Care Organization,Coupon Organization,Extreme Couponing,Couponing 101,Life Binder,Save My Money,Love Coupons",
  "is_image_or_video": "image",
  "image_src": "https://i.pinimg.com/originals/65/bb/ea/65bbeaf458907bb079317d8303c4fa0e.jpg",
  "downloaded": 1,
  "save_location": "Local save in /data/finance",
  "category": "finance"
}
```

geolocation_data:
```
{'ind': 5730, 'timestamp': datetime.datetime(2021, 4, 19, 17, 37, 3), 'latitude': -77.015, 'longitude': -101.437, 'country': 'Colombia'}
```

user_data:
```
{'ind': 5730, 'first_name': 'Rachel', 'last_name': 'Davis', 'age': 36, 'date_joined': datetime.datetime(2015, 12, 8, 20, 2, 43)}
```

## Tools used

- [Apache Kafka](https://kafka.apache.org/) - Apache Kafka is an event streaming platform. From the Kafka [documentation](https://kafka.apache.org/documentation/):
>Event streaming is the practice of capturing data in real-time from event sources like databases, sensors, mobile devices, cloud services, and software applications in the form of streams of events; storing these event streams durably for later retrieval; manipulating, processing, and reacting to the event streams in real-time as well as retrospectively; and routing the event streams to different destination technologies as needed. Event streaming thus ensures a continuous flow and interpretation of data so that the right information is at the right place, at the right time.

- [AWS MSK](https://aws.amazon.com/msk/) - Amazon Managed Streaming for Apache Kafka (Amazon MSK) is a fully managed service that enables you to build and run applications that use Apache Kafka to process streaming data. More information can be found in the [developer guide](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html).

- [AWS MSK Connect](https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect.html) - MSK Connect is a feature of Amazon MSK that makes it easy for developers to stream data to and from their Apache Kafka clusters. From the developer guide:
>With MSK Connect, you can deploy fully managed connectors built for Kafka Connect that move data into or pull data from popular data stores like Amazon S3... Use source connectors to import data from external systems into your topics. With sink connectors, you can export data from your topics to external systems.

- [Kafka REST Proxy](https://docs.confluent.io/platform/current/kafka-rest/index.html) - From the docs:
>The Confluent REST Proxy provides a RESTful interface to an Apache Kafka® cluster, making it easy to produce and consume messages, view the state of the cluster, and perform administrative actions without using the native Kafka protocol or clients.

- [AWS API Gateway](https://aws.amazon.com/api-gateway/) -
>Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services.

- [Apache Spark](https://spark.apache.org/docs/3.4.1/) - Apache Spark™ is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters. From the docs:
>Spark provides high-level APIs in Java, Scala, Python, and R, and an optimized engine that supports general execution graphs. It also supports a rich set of higher-level tools including Spark SQL for SQL and structured data processing, pandas API on Spark for pandas workloads, MLlib for machine learning, GraphX for graph processing, and Structured Streaming for incremental computation and stream processing.

- [PySpark](https://spark.apache.org/docs/3.4.1/api/python/index.html) - PySpark is the Python API for Apache Spark.
>It enables you to perform real-time, large-scale data processing in a distributed environment using Python. It also provides a PySpark shell for interactively analyzing your data. PySpark combines Python’s learnability and ease of use with the power of Apache Spark to enable processing and analysis of data at any size for everyone familiar with Python.

- [Databricks](https://docs.databricks.com/en/index.html) - This project uses the Databricks platform to perform Spark processing of batch and streaming data. From the documentation:
>Databricks is a unified, open analytics platform for building, deploying, sharing, and maintaining enterprise-grade data, analytics, and AI solutions at scale. The Databricks Lakehouse Platform integrates with cloud storage and security in your cloud account, and manages and deploys cloud infrastructure on your behalf.

- [Managed Workflows for Apache Airflow](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) - Apache Airflow enables users to use Python to build scheduling workflows for batch-oriented processes. This project uses MWAA to orchestrate batch processing on the Databricks platform. From AWS docs:
>With Amazon MWAA, you can use Apache Airflow and Python to create workflows without having to manage the underlying infrastructure for scalability, availability, and security.

- [AWS Kinesis](https://aws.amazon.com/kinesis/) - AWS Kinesis is a managed service for processing and analysing streaming data. In this project I've used Kinesis Data Streams to collect and store data temporarily before using Spark on Databricks to read and process the stream.

## Architecture Overview
