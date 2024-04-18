# pinterest-data-pipeline841

## Table of contents
# [Project Description](#project-description)
# [Project Installation and Dependencies](#project-installation-and-dependencies)
# [The Data](#the-data)
Tools used
Architecture Overview
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

# Project Description

This project emulates a Pinterest-like data pipeline to handle real-time user-generated data. The aim is to simulate the process of ingesting, processing, and storing data at scale, using AWS services and Kafka. There are two pipelines built in the project ; 
I. Computing real-time metrics (such as profile popularity, which would be used to recommend that profile in real-time)
II. Computing metrics that depend on historical data (such as the most popular category this year) 
I've learned about the complexities of managing data pipelines in a cloud environment, the importance of data stream partitioning for scalability and fault tolerance, and the intricacies of configuring AWS services and Kafka for real-time data processing. Alongside this technical side, I learned how important adjust the cost. So the architecture should be designed with a focus on scalability and fault tolerance, employing data stream partitioning and optimized resource allocation to efficiently manage data flow and processing tasks. This approach ensured that the system could handle varying data volumes effectively, minimizing costs while maximizing performance.


# Project Installation and Dependencies

The modules need to be installed:

- python-dotenv
- sqlalchemy
- requests

For the Virtual environment; I used the CONDA environment

- Create a Conda environment 
conda create -n your_env_name python=3.x
conda activate your_env_name
pip install -r requirements.txt

# The Data

In order to emulate the kind of data that Pinterest's engineers are likely to work with, this project contains a script, main_user_posting_emulation_cosole_testing.py that when run from the terminal mimics the stream of random data points received by the Pinterest API when POST requests are made by users uploading data to Pinterest.

Running the script instantiates a database connector class, which is used to connect to an AWS RDS database containing the following tables:

- pinterest_data contains data about posts being updated to Pinterest
- geolocation_data contains data about the geolocation of each Pinterest post found in pinterest_data
- user_data contains data about the user that has uploaded each post found in pinterest_data
The methods in each of the main_user_posting_emulation... scripts infinitely iterates at random intervals between 0 and 2 seconds, selecting all columns of a random row from each of the three tables and writing the data to a dictionary. The three dictionaries are then printed to the console.

Examples of the data generated look like the following:

pinterest_data:

```json
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

geolocation_data:

```json
{'ind': 5730, 'timestamp': datetime.datetime(2021, 4, 19, 17, 37, 3), 'latitude': -77.015, 'longitude': -101.437, 'country': 'Colombia'}


user_data:

```json
{'ind': 5730, 'first_name': 'Rachel', 'last_name': 'Davis', 'age': 36, 'date_joined': datetime.datetime(2015, 12, 8, 20, 2, 43)}


## Usage Instructions
(TODO: Include instructions on how to use the system once it's set up, detailing any commands, scripts, or interfaces designed for interacting with the pipeline.)

## File Structure
(TODO: Detail the organization of the project directory, explaining the purpose of main folders and files to help users navigate your project.)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
