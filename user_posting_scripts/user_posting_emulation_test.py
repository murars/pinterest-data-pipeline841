import random

from database_utils import *

@run_infinitely
def run_infinite_post_data_loop():
    '''
    Utilises decorator to run infinitely at random intervals, calls class method
    to get records and then prints those records to the console.
    '''
    # create database connection and get records
    new_connector.connect_and_get_records()
    # generate a random row number between 0 and 11000
    random_row = random.randint(0, 11000)
    # row_index = new_connector.random_row
    print(f"\n\rRow index number: {random_row}\n\r")
    print(new_connector.pin_result)
    print("-"*100)
    print(new_connector.geo_result)
    print("-"*100)
    print(new_connector.user_result)
    print("-"*100)
    # print(type(row_index))

if __name__ == "__main__":
    new_connector = AWSDBConnector()
    print('Working...')
    run_infinite_post_data_loop()
