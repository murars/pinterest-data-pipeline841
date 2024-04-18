import random

from database_utils import *

@just_keep_running
def run_infinite_post_data_loop():
    '''
    Utilises decorator to run infinitely at random intervals, calls class method
    to get records and then prints those records to the console.
    '''
    # generate a random row number between 0 and 11000
    random_row = random.randint(0, 11000)
    # row_index = new_connector.random_row
    print(f"\n\rRow index number: {random_row}\n\r")
    print(new_connector.get_records("pinterest_data", random_row))
    print("-"*100)
    print(new_connector.get_records("geolocation_data", random_row))
    print("-"*100)
    print(new_connector.get_records("user_data", random_row))
    print("-"*100)
    # print(type(row_index))

if __name__ == "__main__":
    new_connector = AWSDBConnector()
    print('Working...')
    run_infinite_post_data_loop()

