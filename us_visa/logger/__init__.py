import logging
import os
from datetime import datetime

LOG_DIR="logs"
LOG_PATH=os.path.join(os.getcwd(),LOG_DIR)
os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}"
file_name=f"log_{LOG_FILE}.log"
logs_path=os.path.join(LOG_DIR,file_name)

logging.basicConfig(filename=logs_path,
                    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
                    level=logging.DEBUG)