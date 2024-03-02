import sys
from us_visa.exception import USVisaException
from us_visa.logger import logging

import os
from us_visa.constants import DATABASE_NAME,MONGODB_URL_KEY
import pymongo


class MongoDBClient:
    client=None

    def __init__(self,database_name=DATABASE_NAME)->None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key:{MONGODB_URL_KEY} is not set.")
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url)
            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            logging.info("MongoDB connection successful")
        except Exception as e:
            raise USVisaException(e,sys)