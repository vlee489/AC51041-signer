import logging
from app.functions.env import EnvVars
env = EnvVars()

# Initialize logging
logging.basicConfig(
    level=(
        logging.DEBUG if env.debug else logging.INFO
    ),
    format='\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mon\033[0m %(asctime)s\033[90m:\033[0m %(message)s',
    datefmt='\033[32m%m/%d/%Y\033[0m \033[90mat\033[0m \033[32m%H:%M:%S\033[0m'
)