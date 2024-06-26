# pinterest-data-pipeline841

## Table of contents

- [Project Description](#project-description)
- [Project Installation and Dependencies](#project-installation-and-dependencies)
- [The Data](#the-data)
- [Tools used](#tools-used)
- [Architecture Overview](#architecture-overview)
- [Building the pipeline](#building-the-pipeline)
  - [Create an Apache cluster using AWS MSK](#create-an-apache-cluster-using-aws-msk)
  - [Create a client machine for the cluster](#create-a-client-machine-for-the-cluster)
  - [Enable client machine to connect to the cluster](#enable-client-machine-to-connect-to-the-cluster)
  - [Install Kafka on the client machine](#install-kafka-on-the-client-machine)
  - [Create topics on the Kafka cluster](#create-topics-on-the-kafka-cluster)
  - [Delivering messages to the Kafka cluster](#delivering-messages-to-the-kafka-cluster)
  - [AWS API Gateway](#aws-api-gateway)
  - [Sending messages to the cluster using the API gateway](#sending-messages-to-the-cluster-using-the-api-gateway)
  - [Connecting the Apache cluster to AWS S3 bucket](#connecting-the-apache-cluster-to-aws-s3-bucket)
- [Batch processing data using Apache Spark on Databricks](#batch-processing-data-using-apache-spark-on-databricks)
  - [Clean and query the data using Apache Spark on Databricks](#clean-and-query-the-data-using-apache-spark-on-databricks)
  - [Orchestrating automated workflow of notebook on Databricks](#orchestrating-automated-workflow-of-notebook-on-databricks)
- [Processing streaming data](#processing-streaming-data)
  - [Create data streams on Kinesis](#create-data-streams-on-kinesis)
  - [Create API proxy for uploading data to streams](#create-api-proxy-for-uploading-data-to-streams)
  - [Sending data to the Kinesis streams](#sending-data-to-the-kinesis-streams)
  - [Processing the streaming data in Databricks](#processing-the-streaming-data-in-databricks)
- [Next steps](#next-steps)


## Project Description

This project emulates a Pinterest-like data pipeline to handle both batch and real-time user-generated data. The aim is to simulate the process of ingesting, processing, and storing data at scale, using AWS services. The project involves building two pipelines:

I. Batch Data Metrics with Kafka: This pipeline processes batch data using Kafka for computing metrics that depend on historical data. For example, it calculates metrics such as the most popular category over time. Kafka facilitates the ingestion and processing of batch data in a fault-tolerant and scalable manner, enabling historical analysis and insights.

II. Real-time Metrics with Kinesis: This pipeline computes real-time metrics, such as profile popularity, leveraging Kinesis for streaming data ingestion and processing. It enables efficient handling of real-time user interactions and allows for immediate insights into user behavior.

Through this project, I gained insights into managing data pipelines in a cloud environment, understanding the nuances of both streaming and batch processing technologies. I learned the importance of optimizing resource allocation and adjusting costs in the cloud architecture design. The architecture was crafted with scalability and fault tolerance in mind, employing data stream partitioning and optimized resource allocation to ensure efficient data flow and processing across both pipelines. This approach enabled the system to handle varying data volumes effectively, while minimizing costs and maximizing performance.


## Project Installation and Dependencies

The modules need to be installed:

- `python-dotenv`
- `sqlalchemy`
- `requests`

For the Virtual environment; CONDA environment is used 

- Create a Conda environment 
`conda create -n pinterest_project_env python=3.x`
`conda activate pinterest_project_env`
`pip install -r requirements.txt`


## The Data

To emulate the kind of data that Pinterest's engineers are likely to work with, this project contains a script, [user_posting_emulation_test.py](user_posting_emulation_test.py) that when run from the terminal mimics the stream of random data points received by the Pinterest API when POST requests are made by users uploading data to Pinterest.

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
![Architecture Overview](images/CloudPinterestPipeline.png)


## Building the pipeline

### Create an Apache cluster using AWS MSK

The first stop in the pipeline for our data will be an Apache Kafka cluster in the AWS cloud ecosystem, using Amazon Managed Streaming for Apache Kafka (MSK). The documentation includes a good guide for getting started and I will outline the steps taken to get a cluster up and running here.

1. Firstly, log into the AWS console and navigate to MSK via the 'Services' menu.
2. From the MSK menu, click on 'Create cluster' to start the process.
3. Here, choose from 'quick' or 'custom' create options and name the cluster:

<img src="images/apache-msk-1.png" alt="Create an Apache cluster using AWS MSK" width="600px">


4. Scroll down and choose 'Provisioned' and specify the Kafka version and broker type. The type chosen will depend on requirements and cost considerations.
  
<img src="images/apache-msk-2.png" alt="Create an Apache cluster using AWS MSK" width="600px">

5. Finally, scroll down and click 'Create cluster'. The cluster can take between 15 and 20 minutes to create. When the cluster has been created, navigate to the 'Properties' tab, locate the network settings and take a note of the security group associated with the cluster. Next, click on 'View client information' and take a note of the bootstrap servers.

### Create a client machine for the cluster

1. Once the cluster is up and running, a client is needed to communicate with it. In this project, an EC2 instance is used to act as the client.

Navigate to the EC2 dashboard and click on 'Launch Instance':

<img src="images/ec2-launch-instance.png" alt="Create a client machine for the cluster" width="600px">

2. Give the instance a name, e.g. 'pinterest-kafka-client'.
3. Keep the default Application and OS images, and instance type. Again, this choice may be determined by usage and cost considerations.

<img src="images/ec2-OS-images.png" alt="Create a client machine for the cluster" width="600px">

4. Create a new keypair for connecting securely to the instance via SSH. Give the keypair a descriptive name and choose 'RSA' and '.pem' for the type and file format, respectively. The .pem file will automatically download - keep this file safe for later use.

<img src="images/ec2-key-pair.png" alt="Create a client machine for the cluster" width="600px">

5. Keep the default settings for the other sections. Click on 'Launch Instance' in the right-hand summary menu.

### Enable client machine to connect to the cluster

In order for the client machine to connect to the cluster, we need to edit the inbound rules for the security group associated with the cluster.

1. In the left-hand EC2 menu, click on 'Security Groups'.
2. Select the security group associated with the Kafka cluster (noted earlier).
3. Select the 'Inbound rules' tab and then click on 'Edit inbound rules'.
4. Click on 'Add rule'. Choose 'All traffic' for the type, and then select the security group associated with the EC2 instance.
5. Save the rules.
   
We also need to create an IAM role for the client machine.

1. Navigate to the AWS IAM dashboard, select 'Roles' from the left-hand menu and then click on 'Create role'.
2. Select 'AWS service' and 'EC2', then click on 'Next'.
3. On the next page, select 'Create policy'.
4. In the policy editor, choose JSON format and paste in the following policy. Note: this policy is somewhat open - a more restrictive policy would be more appropriate for a production environment
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "kafka:ListClustersV2",
                "kafka:ListVpcConnections",
                "kafka:DescribeClusterOperation",
                "kafka:GetCompatibleKafkaVersions",
                "kafka:ListClusters",
                "kafka:ListKafkaVersions",
                "kafka:GetBootstrapBrokers",
                "kafka:ListConfigurations",
                "kafka:DescribeClusterOperationV2"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "kafka-cluster:*",
            "Resource": [
                "arn:aws:kafka:*:<AWS-UUID>:transactional-id/*/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:group/*/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:topic/*/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:cluster/*/*"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "kafka:*",
            "Resource": [
                "arn:aws:kafka:*:<AWS-UUID>:cluster/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:configuration/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:vpc-connection/*/*/*"
            ]
        }
    ]
}
```

5. On the next page, give the policy a descriptive name and save the policy.
6. Back in the create role tab in the browser, click refresh to show the new policy and select the policy.
7. Click 'Next', give the role a descriptive name and save the role.
8. In the EC2 dashboard, click on the client instance.
9. Under 'Actions' and 'Security', click on 'Modify IAM role'.
10. Select the role just created and click on 'Update IAM role'.

### Install Kafka on the client machine

1. Once the new instance is in the running state, connect via SSH to interact with the instance using the command line. To do this, click on the instance ID to open the summary page, then click on 'Connect':

<img src="images/connect-to-ec2.png" alt="Install Kafka on the client macine" width="700px">

2. Follow the instructions in the 'SSH' tab to connect to the instance.
```
# make sure key is not publicly viewable
chmod 400 pinterest-kafka-client-keypair.pem
# connect
ssh -i "pinterest-kafka-client-keypair.pem" ec2-user@<instance-public-DNS>
```
3. Now on the instance command line:
```
# install Java - required for Kafka to run
sudo yum install java-1.8.0
# download Kafka - must be same version as MSK cluster created earlier
wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
# unpack .tgz
tar -xzf kafka_2.12-2.8.1.tgz
```

4. Install the [MSK IAM package](https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar) that will enable the MSK cluster to authenticate the client:

```
# navigate to the correct directory
cd kafka_2.12-2.8.1/libs/
# download the package
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar
```

5. Configure the client to be able to use the IAM package:
```
# open bash config file
nano ~/.bashrc
```

Add the following line to the config file, then save and exit:

  export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
  
Continue with configuration:
```
# activate changes to .bashrc
source ~/.bashrc
# navigate to Kafka bin folder
cd ../bin
# create client.properties file
nano client.properties
```
Add the following code to the client.properties file, then save and exit:
```
# Sets up TLS for encryption and SASL for authN.
security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required;

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

### Create topics on the Kafka cluster

It is now possible to create topics on the Kafka cluster using the client machine command line. The command for creating topics is as follows. Use the boostrap server string noted earlier after cluster creation.
    
```
<path-to-your-kafka-installation>/bin/kafka-topics.sh --create --bootstrap-server <BootstrapServerString> --command-config client.properties --topic <topic name>
```
For this project, I created three topics. One each for the pinterest_data, geolocation_data, and user_data outlined above.

### Delivering messages to the Kafka cluster

Now that our cluster is up and running, and the client is configured to access the cluster and create topics, it's possible to use the client to create producers for streaming messages to the cluster, and consumers for accessing those messages.

However, for this project I used the Confluent package to set up a REST API on the client that listens for requests and interacts with the Kafka cluster accordingly.

To do this, first download the Confluent package to the client from the client's command line:
```
# download package
sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
# unpack .tar
tar -xvzf confluent-7.2.0.tar.gz
```
Next, modify the kafka-rest.properties file:

```
# navigate to the correct directory
cd confluent-7.2.0/etc/kafka-rest/
nano kafka-rest.properties
```
Change the bootstrap.servers and the zookeeper.connect variables to those found in the MSK cluster information. Add the following lines to allow authentication:

```
# Sets up TLS for encryption and SASL for authN.
client.security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
client.sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
client.sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required;

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```
The inbound rules for the client security group also need to be modified to allow incoming HTTP requests on port 8082. On the AWS 'Security groups' page, choose the security group attached to the client, and add the following inbound rule:

<img src="images/client-http-inbound-rules.png" alt="Delivering messages to the Kafka cluster" width="800px">

To start the REST API, navigate to the confluent-7.2.0/bin folder and run the following command:

```
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
```

The API's ability to receive requests can be tested by opening a web browser and going to "http://your-client-public-dns:8082/topics". The response should be displayed in the browser window and look something like:

```
["data.pin","data.user","__amazon_msk_canary","data.geo"]
```

For this project, to more easily connect to the API programmatically using different request methods I set up an API gateway on AWS

### AWS API Gateway

Navigate to the AWS API Gateway service. This project uses a REST API.

1. Click on 'Build' in the REST API box:

<img src="images/rest-api-build.png" alt="AWS API Gateway" width="900px">

2. Choose 'REST', 'New API', give the API a descriptive name, then click on 'Create API':

<img src="images/rest-api-build-2.png" alt="AWS API Gateway" width="600px">

3. From the 'Actions' menu, choose 'Create resource'. Select 'Configure as proxy resource' and 'Enable API Gateway CORS' boxes, then click on 'Create resource':

<img src="images/rest-api-create-resource.png" alt="AWS API Gateway" width="600px">

4. On the next page, set up HTTP Proxy, using the address for earlier as the endpoint, "http://your-client-public-dns:8082/{proxy}":

<img src="images/rest-api-create-method.png" alt="AWS API Gateway" width="600px">

5. With the resource and method created, it's possible to test the API (make sure that the REST proxy on the client is running and listening for requests). If everything is working correctly, the following test should result in a 200 response code and the same response body obtained through the browser:

<img src="images/rest-api-test-method.png" alt="AWS API Gateway" width="600px">

6. Now the API needs to be deployed. From the 'Actions' menu, select 'Deploy API'. Choose 'New stage' and give the stage a name, then click on 'Deploy':

<img src="images/rest-api-deploy.png" alt="AWS API Gateway" width="400px">

This completes the process and an invoke URL is generated that can then be used for POST requests.

### Sending messages to the cluster using the API gateway

Running the script [user_posting_emulation_batch_kafka.py](user_posting_scripts/user_posting_emulation_batch_kafka.py) will emulate a stream of messages and post those messages to the cluster via the API gateway and the Kafka REST proxy.

In order to access the messages in each topic in the cluster, I have used Kafka Connect, using AWS MSK Connect, to connect the cluster to an AWS S3 bucket into which messages can be deposited.


### Connecting the Apache cluster to AWS S3 bucket

To start with, create an S3 bucket that will connect to the cluster.

1. From the AWS S3 dashboard, select 'Create bucket'
2. Give the bucket a descriptive name (must be unique) and make sure the bucket is in the same AWS region as the rest of the project resources. Keep other settings as default.

Next, create an IAM role for the MSK connector using the following policy. Again, this policy may not be restrictive enough for production purposes. I am using this for development only.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "kafka-cluster:DescribeCluster",
                "kafka-cluster:Connect"
            ],
            "Resource": [
                "arn:aws:s3:::<BUCKET-NAME>",
                "arn:aws:s3:::<BUCKET-NAME>/*",
                "arn:aws:kafka:<REGION>:<AWS-UUID>:cluster/<CLUSTER-NAME>/<CLUSTER-UUID>"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:ReadData",
                "kafka-cluster:DescribeTopic"
            ],
            "Resource": "arn:aws:kafka:<REGION>:<AWS-UUID>:topic/<CLUSTER-NAME>/<CLUSTER-UUID>/*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:DescribeTopic",
                "kafka-cluster:WriteData"
            ],
            "Resource": "arn:aws:kafka:<REGION>:<AWS-UUID>:topic/<CLUSTER-NAME>/<CLUSTER-UUID>/*"
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:CreateTopic",
                "kafka-cluster:ReadData",
                "kafka-cluster:DescribeTopic",
                "kafka-cluster:WriteData"
            ],
            "Resource": "arn:aws:kafka:<REGION>:<AWS-UUID>:topic/<CLUSTER-NAME>/<CLUSTER-UUID>/__amazon_msk_connect_*"
        },
        {
            "Sid": "VisualEditor4",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:AlterGroup",
                "kafka-cluster:DescribeGroup"
            ],
            "Resource": [
                "arn:aws:kafka:<REGION>:<AWS-UUID>:group/<CLUSTER-NAME>/<CLUSTER-UUID>/__amazon_msk_connect_*",
                "arn:aws:kafka:<REGION>:<AWS-UUID>:group/<CLUSTER-NAME>/<CLUSTER-UUID>/connect-*"
            ]
        },
        {
            "Sid": "VisualEditor5",
            "Effect": "Allow",
            "Action": [
                "s3:ListStorageLensConfigurations",
                "s3:ListAccessPointsForObjectLambda",
                "s3:GetAccessPoint",
                "s3:PutAccountPublicAccessBlock",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:ListAccessPoints",
                "s3:PutAccessPointPublicAccessBlock",
                "s3:ListJobs",
                "s3:PutStorageLensConfiguration",
                "s3:ListMultiRegionAccessPoints",
                "s3:CreateJob"
            ],
            "Resource": "*"
        }
    ]
}
```
The role should have the following trust relationship:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "kafkaconnect.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

The next step is to create a VPC endpoint to S3. From the VPC dashboard in AWS, select 'Endpoints' from the left-hand menu then click on 'Create endpoint'. Give the endpoint a descriptive name, then select 'AWS services'. Search for 'S3' in the 'Services' search field, then select:

<img src="images/vpc-endpoint.png" alt="Connecting the Apache cluster to AWS S3 bucket" width="900px">

Choose the default VPC for the region, click the check box next to the default route tables, then click on 'Create endpoint'.

We're now ready to create the connector. The first step is to create a new plugin for the connector.

1. To create the plugin, a .zip file with the plugin files is required. For the Kafka S3 Sink Connector, this can be downloaded from ["https://www.confluent.io/hub/confluentinc/kafka-connect-s3"](https://www.confluent.io/hub/confluentinc/kafka-connect-s3). Once downloaded, it should be uploaded to the S3 bucket, either via the console or via a web browser.
2. In the AWS MSK dashboard, select 'Custom plugins' from the left-hand menu, then click on 'Create custom plugin'.
3. In the next window, navigate to the S3 bucket where the .zip is stored, and select the .zip file:

<img src="images/custom-plugin.png" alt="Connecting the Apache cluster to AWS S3 bucket" width="600px">

4. Click on 'Create custom plugin'. The process will take a few minutes.

Now create the connector. Navigate to 'Connectors' in the left-hand menu of the MSK dashboard.
1. Click on 'Create connector'.
2. Select 'Use existing plugin' and select the plugin just created. Click 'Next'.
3. Give the connector a name, make sure 'MSK cluster' is highlighted, then select the cluster created earlier.
4. Use the following settings for the configuration:

```
connector.class=io.confluent.connect.s3.S3SinkConnector
# same region as our bucket and cluster
s3.region=<REGION>
flush.size=1
schema.compatibility=NONE
tasks.max=3
# this depends on names given to topics
topics.regex=<TOPIC-NAME>.*
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
value.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.json.JsonConverter
storage.class=io.confluent.connect.s3.storage.S3Storage
key.converter=org.apache.kafka.connect.storage.StringConverter
s3.bucket.name=<BUCKET_NAME>
```

5. Choose defaults for remaining settings until 'Access Permissions', where the IAM role created for the connector should be selected.
6. Click 'Next', then 'Next' again. Select a location for log delivery. I selected to have logs delivered to the S3 bucket.
7. Click 'Next' and then 'Create connector'.

Once the connector creation process is complete, you should be able to see any messages sent to the cluster in the S3 bucket, inside a folder named 'Topics'.

## Batch processing data using Apache Spark on Databricks

In order to batch process the data on Databricks, it's necessary to mount the S3 bucket on the platform. The file [mounting_the_S3_bucket_on_the_databricks.ipynb](databricks_notebooks/mounting_the_S3_bucket_on_the_databricks.ipynb) is a notebook that was run on the Databricks platform. The steps carried out in the notebook are:

1. Import necessary libraries
2. List tables in Databricks filestore in order to obtain AWS credentials file name
3. Read the credentials .csv into a Spark dataframe
4. Generate credential variables from Spark dataframe
5. Mount the S3 bucket containing the messages from the Kafka topics
6. List the topics
7. Read the .json message files into three Spark dataframes, one each for each of the topics

### Clean and query the data using Apache Spark on Databricks

The file [clean_and_queries_batch_data.ipynb](databricks_notebooks/clean_and_queries_batch_data.ipynb) contains the code for performing the necessary cleaning and querying of the dataframes created using the steps above. 

### Orchestrating automated workflow of notebook on Databricks

MWAA was used to automate the process of running the batch processing on Databricks. The file [0ecac53030fd_dag.py](0ecac53030f_dag.py) is the Python code for a directed acyclic graph (DAG) that orchestrates the running of the batch processing notebook described above. The file was uploaded to the MWAA environment, where Airflow is utilised to connect to and run the Databricks notebook at scheduled intervals, in this case @daily.

## Processing streaming data

### Create data streams on Kinesis
The first step in processing streaming data was to create three streams on AWS Kinesis, one for each of the data sources.

  1. From the Kinesis dashboard, select 'Create data stream'.

<img src="images/kinesis-dashboard.png" alt="Create data streams on Kinesis" width="600px">

  2. Give the stream a name, and select 'Provisioned' capacity mode.

<img src="images/create-stream.png" alt="Create data streams on Kinesis" width="900px">

  3. Click on 'Create data stream' to complete the process.

### Create API proxy for uploading data to streams
It's possible to interact with the Kinesis streams using HTTP requests. In order to do this with the streams just added to Kinesis, I created new API resources on AWS API Gateway.

The settings used for the DELETE method were:

 - 'Integration Type': 'AWS Service'
 - 'AWS Region': 'us-east-1'
 - 'AWS Service': 'Kinesis'
 - 'HTTP method': 'POST'
 - 'Action': 'DeleteStream'
 - 'Execution role': 'arn of IAM role created'

<img src="images/delete-method-settings-1.png" alt="Create API proxy for uploading data to streams" width="900px">

In 'Integration Request' under 'HTTP Headers', add a new header:

 - 'Name': 'Content-Type'
 - 'Mapped from': 'application/x-amz-json-1.1'
 - 
Under 'Mapping Templates', add new mapping template:
 - 'Content Type': 'application/json'

Use the following code in the template:
```
{
    "StreamName": "$input.params('stream-name')"
}
```
<img src="images/delete-method-settings-2.png" alt="Create API proxy for uploading data to streams" width="900px">

For the other methods, the same settings were used except for:

 - GET
  - 'Action': 'DescribeStream'
  - 'Mapping Template':
``` 
{
    "StreamName": "$input.params('stream-name')"
}
```

 - POST
  - 'Action': 'CreateStream'
  - 'Mapping Template':
```
{
    "ShardCount": #if($input.path('$.ShardCount') == '') 5 #else $input.path('$.ShardCount') #end,
    "StreamName": "$input.params('stream-name')"
}
```

/record

 - PUT
  - 'Action': 'PutRecord'
  - 'Mapping Template':
```
{
    "StreamName": "$input.params('stream-name')",
    "Data": "$util.base64Encode($input.json('$.Data'))",
    "PartitionKey": "$input.path('$.PartitionKey')"
}
```

/records

 - PUT
  - 'Action': 'PutRecords'
  - 'Mapping Template':
```
{
    "StreamName": "$input.params('stream-name')",
    "Records": [
       #foreach($elem in $input.path('$.records'))
          {
            "Data": "$util.base64Encode($elem.data)",
            "PartitionKey": "$elem.partition-key"
          }#if($foreach.hasNext),#end
        #end
    ]
}
```

After creating the new resources and methods, the API must be redeployed.

### Sending data to the Kinesis streams

Running the script [user_posting_emulation_streaming.py](user_posting_scripts/user_posting_emulation_streaming.py) starts an infinite loop that, like in the examples above, retrieves records from the RDS database and sends them via the new API to Kinesis.

### Processing the streaming data in Databricks

The Jupyter notebook [read_and_transform_Kinesis_streams.ipynb](databricks_notebooks/read_and_transform_Kinesis_streams.ipynb) contains all the code necessary for retrieving the streams from Kinesis, transforming (cleaning) the data, and then loading the data into Delta tables on the Databricks cluster. The steps taken in the code are:

  1. Import necessary functions and types
  2. List tables in Databricks filestore in order to obtain AWS credentials file name
  3. Read the credentials .csv into a Spark dataframe
  4. Generate credential variables from Spark dataframe
  5. Define functions for:
    - getting streams from Kinesis using spark.readStream - returns dataframe with stream info and data in binary format
    - deserialising the stream data - converts the binary data format to a dataframe using schema defined above
    - writing streaming data to Delta tables using Spark writeStream function
  6. Define schema for deserialised data
  7. Invoke get_stream function for all three streams
  8. Invoke deserialise_stream function for all three streams
  9. Clean all three streams
  10. Display the streams
  11. Write the streams to Delta tables

### To access and verify the data in Databricks, follow these steps:

  - Navigate to Databricks off the main menu on the left.
  - Click on "Catalog."
 <img src="images/checking-data-delta-table-1.png" alt="To access and verify the data in Databricks" width="800px">
 
  - Locate your streaming name among the available tables:
    - 0ecac53030rd_pin_table
    - 0ecac53030rd_geo_table
    - 0ecac53030rd_user_table
  - Click on each table, and inside the table, click on "Sample Data."
  - Verify if the data displayed is cleaned data, meaning it has been processed and is ready for analysis.

<img src="images/checking-data-delta-table-2.png" alt="To access and verify the data in Databricks" width="900px">

## Next Steps:

Considering Further Data Analysis:
   - Querying the streaming data for deeper insights and analysis. 
   - Visualize the data using a visualization tool such as Tableau or Power BI to create interactive dashboards and reports.

