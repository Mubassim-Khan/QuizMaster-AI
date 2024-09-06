import logging
import os
from datetime import datetime

# Name of Log file to be generated
Log_File = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a folder 'logs' & store all log files in there
log_path = os.path.join(os.getcwd(),"logs")

os.makedirs(log_path,exist_ok=True)

LOG_FILEPATH = os.path.join(log_path,Log_File)

logging.basicConfig(level = logging.INFO, 
        filename = LOG_FILEPATH,
        format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)