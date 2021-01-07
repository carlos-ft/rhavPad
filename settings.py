import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG = True
# Application definition

#REDIS
REDIS_HOST = 'redis'
REDIS_PORT = 6379