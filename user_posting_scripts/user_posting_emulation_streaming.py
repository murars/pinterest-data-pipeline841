from database_utils import *

new_connector = AWSDBConnector()

@run_infinitely
def run_infinite_post_data_loop():
    '''
    Utilises decorator to run infinitely at random intervals, calls class method
    to get records and then posts the records to the Kinesis streams.
    '''
    new_connector.connect_and_get_records()
    # post result to Kinesis stream via API
    post_record_to_API("PUT", "https://ib9giyafm5.execute-api.us-east-1.amazonaws.com/prod/streams/streaming-0ecac53030fd-pin/record", new_connector.pin_result, "streaming-0ecac53030fd-pin")
    post_record_to_API("PUT", "https://ib9giyafm5.execute-api.us-east-1.amazonaws.com/prod/streams/streaming-0ecac53030fd-geo/record", new_connector.geo_result, "streaming-0ecac53030fd-geo")
    post_record_to_API("PUT", "https://ib9giyafm5.execute-api.us-east-1.amazonaws.com/prod/streams/streaming-0ecac53030fd-user/record", new_connector.user_result, "streaming-0ecac53030fd-user")    
    
if __name__ == "__main__":
    print('Working')
    run_infinite_post_data_loop()
    
