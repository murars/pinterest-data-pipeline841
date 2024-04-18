import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import random
from time import sleep
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class AWSDBConnector:
    """Manage database connections and queries to AWS RDS."""

    def __init__(self):
        self.host = os.getenv('RDSHOST')
        self.user = os.getenv('RDSUSER')
        self.password = os.getenv('RDSPASSWORD')
        self.database = os.getenv('RDSDATABASE')
        self.port = os.getenv('RDSPORT')
        self.engine = self.create_db_connector()
        self.Session = sessionmaker(bind=self.engine)
    
    def create_db_connector(self):
        """Creates a database engine connection."""
        connection_string = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8mb4"
        return create_engine(connection_string, echo=True, pool_pre_ping=True)

    def get_records(self, table: str, row_number):
        engine = self.create_db_connector()
        with engine.connect() as connection:
            query_string = text(f"SELECT * FROM {table} LIMIT {row_number}, 1")
            selected_row = connection.execute(query_string)
            for row in selected_row:
                result = dict(row._mapping)
            return result
# Decorator function
def just_keep_running(func):
    '''
    Decorator to run function infinitely at random intervals between 0 and 2 seconds.
    '''
    def inner():
        random.seed(100)  # seed for reproducible 'random' results
        post_count = 0  # counts cycles of the function
        while True:  # can use "while post_count < x:" where x is number of runs
            sleep(random.randrange(0, 2))  # pause for a random length of time between 0 and 2 seconds
            try:
                func()
            except Exception as e:
                logging.error(f"Error during function execution: {e}")
            post_count += 1
            if post_count % 10 == 0:
                logging.info(f"{post_count} posts loaded")
    return inner