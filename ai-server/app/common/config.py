import os, random, string
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class BaseConfig():
    
    FINSECURED_SECRET_KEY = os.getenv('FINSECURED_SECRET_KEY', None)

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)

    COHERE_API_KEY = os.getenv('COHERE_API_KEY', None)

    QDRANT_URL = os.getenv('QDRANT_URL', None)
    
    