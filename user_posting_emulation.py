import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:
    """
        Class to handle AWS RDS MySQL database connection details.
    """
    def __init__(self):
        """
            Constructor to initialize connection details.
        """
        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        """
            Method to create a SQLAlchemy engine for MySQL database connection.
        """
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine

# Instantiate the AWSDBConnector class
new_connector = AWSDBConnector()

def send_data_to_Kafka(data, topic, payload):
    """
        Send data to Kafka via HTTP POST request.

        Parameters:
        - data: Data to be sent to Kafka.
        - topic: Kafka topic to publish the data to.
        - payload: JSON payload to be sent in the POST request.
    """
    invoke_url = "https://kgbvktyl9l.execute-api.us-east-1.amazonaws.com/test"
    url = invoke_url + "/topics/" + topic
    print (url)

    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    response = requests.request("POST",url, headers = headers, data = payload)
    print (response.status_code)

    return 


def run_infinite_post_data_loop():
    """
        Run an infinite loop to periodically fetch data from MySQL and send it to Kafka.
    """
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()
        try:
            with engine.connect() as connection:
                # Fetch data from Pinterest table
                pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
                pin_selected_row = connection.execute(pin_string)

                for row in pin_selected_row:
                    pin_result = dict(row._mapping)
                    topic_name = "0a2528ba1237.pin"
                    payload = json.dumps({
                    "records": [
                        {   
                        "value": {"index": pin_result["index"], 
                                "unique_id": pin_result["unique_id"], 
                                "title": pin_result["title"], 
                                "description": pin_result["description"], 
                                "poster_name": pin_result["poster_name"], 
                                "follower_count": pin_result["follower_count"], 
                                "tag_list": pin_result["tag_list"], 
                                "is_image_or_video": pin_result["is_image_or_video"], 
                                "image_src": pin_result["image_src"], 
                                "downloaded": pin_result["downloaded"], 
                                "save_location": pin_result["save_location"], 
                                "category": pin_result["category"]}
                            }
                        ]
                    })
                    send_data_to_Kafka(pin_result, topic_name, payload)
                    print ("pin result sent")
                
           
                # Fetch data from GeoLocation table
                geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
                geo_selected_row = connection.execute(geo_string)

                for row in geo_selected_row:
                    geo_result = dict(row._mapping)
                    topic_name = "0a2528ba1237.geo"
                    payload = json.dumps({
                    "records": [
                        {   
                        "value": {"ind": geo_result["ind"], 
                                "timestamp": geo_result["timestamp"].isoformat(), 
                                "latitude": geo_result["latitude"], 
                                "longitude": geo_result["longitude"], 
                                "country": geo_result["country"]}
                            }
                        ]
                    })

                    send_data_to_Kafka(geo_result, topic_name, payload)
                    print ("geo result sent")
                
               # Fetch data from UserData table
                user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
                user_selected_row = connection.execute(user_string)

                for row in user_selected_row:
                    user_result = dict(row._mapping)
                    topic_name = "0a2528ba1237.user"
                    payload = json.dumps({
                    "records": [
                        {   
                        "value": {"ind": user_result["ind"], 
                                "first_name": user_result["first_name"], 
                                "last_name": user_result["last_name"], 
                                "age": user_result["age"], 
                                "date_joined": user_result["date_joined"].isoformat()}
                            }
                        ]
                    })
                    send_data_to_Kafka(user_result, topic_name, payload)
                    print ("user result sent")
                
                # print(pin_result)
                # print(geo_result)
                # print(user_result)
        except Exception as e:
                    print(f"Error: {e}")
        finally:
                    # Ensure that the connection is closed even if an exception occurs
                    engine.dispose()



if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    
    


