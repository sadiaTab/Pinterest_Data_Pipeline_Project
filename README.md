# Pinterest Data Pipeline

## Project Description

Pinterest crunches billions of data points every day to decide how to provide more value to their users. 
Pinterest utilizes state-of-the-art machine learning engineering systems, handling billions of daily user interactions like image uploads and clicks. These interactions require daily processing to inform decision-making. 
Aim of this project is to develop a system mirroring Pinterest's data analysis infrastructure, capable of analysing both historical and real-time data generated by user posts.

## Technologies Used
The tools used for this project are listed below:

1. **Apache Kafka:**
   - *Description:* Event streaming platform for real-time data capture and processing from various sources.
   - *Documentation:* [Apache Kafka Documentation](https://kafka.apache.org/documentation/)

2. **Amazon MSK (Managed Streaming for Apache Kafka):**
   - *Description:* Fully managed service on AWS for building applications using Apache Kafka for streaming data processing.
   - *Documentation:* [Amazon MSK Documentation](https://docs.aws.amazon.com/msk/)

3. **AWS MSK Connect:**
   - *Description:* Feature of Amazon MSK facilitating easy streaming of data to and from Apache Kafka clusters with managed connectors.
   - *Documentation:* [MSK Connect Documentation](https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect.html)

4. **Kafka REST Proxy:**
   - *Description:* Provides a RESTful interface for interacting with an Apache Kafka cluster, simplifying message production, consumption, and administrative tasks.
   - *Documentation:* [Confluent REST Proxy Documentation](https://docs.confluent.io/platform/current/kafka-rest/)

5. **AWS API Gateway:**
   - *Description:* Fully managed service for creating, publishing, maintaining, monitoring, and securing APIs at scale.
   - *Documentation:* [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)

6. **Apache Spark:**
   - *Description:* Multi-language engine for executing data engineering, data science, and machine learning tasks on single-node machines or clusters.
   - *Documentation:* [Apache Spark Documentation](https://spark.apache.org/documentation.html)

7. **PySpark:**
   - *Description:* Python API for Apache Spark, enabling real-time, large-scale data processing in a distributed environment using Python.
   - *Documentation:* [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

8. **Databricks:**
   - *Description:* Unified, open analytics platform for building, deploying, sharing, and maintaining enterprise-grade data, analytics, and AI solutions at scale.
   - *Documentation:* [Databricks Documentation](https://docs.databricks.com/)

9. **Managed Workflows for Apache Airflow (MWAA):**
   - *Description:* AWS service allowing the use of Apache Airflow and Python to create workflows without managing underlying infrastructure.
   - *Documentation:* [MWAA Documentation](https://docs.aws.amazon.com/mwaa/)

10. **AWS Kinesis:**
    - *Description:* Managed service for processing and analyzing streaming data.
    - *Documentation:* [AWS Kinesis Documentation](https://aws.amazon.com/kinesis/)



## Data Pipeline Building Process

1. Downloaded Pinterest Infrastructure, representing data similar to what the Pinterest API receives when a user uploads data through a post request. The infrastructure comprises three tables: -pinterest_data -geolocation_data -user_data

2. Established the configuration of an EC2 instance as an Apache Kafka client machine for the purpose of creating topics. Subsequently, configured MSK Connect to enable the MSK cluster to transmit data to an S3 bucket, ensuring that any data sent to the topic is automatically saved and stored in a designated S3 bucket. 

![Loading Data](https://github.com/sadiaTab/Pinterest_Data_Pipeline_Project/blob/3004873a47326308f0c2529e3a388392fc052b4b/CloudPinterestPipeline.jpeg)?raw=true)

3. Established an API within AWS API Gateway designed to transmit data to the MSK cluster through the MSK connect connector. Implemented a Kafka REST proxy integration method for the API and configured the Kafka REST proxy on my EC2 client. Activated the REST proxy on the EC2 client machine and adapted the user_posting_emulation.py script to dispatch data to my API. This, in turn, directs the data to the MSK Cluster using the previously established plugin-connector pair, ultimately storing the data in the designated S3 bucket.

4. Retrieve data from AWS into Databricks for batch processing. Utilize Spark on Databricks to clean and perform computations. To facilitate cleaning and querying of batch data, it's necessary to read the data from the S3 bucket into Databricks. Initially, the S3 bucket must be mounted to the Databricks account. Given full access to S3 on the Databricks account and the pre-updated credentials, there's no requirement to generate a new Access Key and Secret Access Key for Databricks.

5. Orchestrated Databricks workloads on AWS MWAA by uploading a Directed Acyclic Graph (DAG) to an MWAA environment and initiating its execution at a specified time.

6. Imported data into Databricks for stream processing. Transmitted data to Kinesis streams, processed and transformed it using Databricks, and recorded the streaming data into Delta tables. Configured the pre-existing REST API to enable invocation of Kinesis actions. The API now has the capability to:
List streams in Kinesis;
Create, describe, and delete streams in Kinesis;
Append records to streams in Kinesis;
Utilized the user_posting_emulation_streaming script to send requests to my API, adding one record at a time to the created streams.

7. Processed and transformed the data within Databricks. Subsequently, saved each stream into a Delta table.

