import os, random, string
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class BaseConfig():
    
    FINSECURED_API_KEY = os.getenv('FINSECURED_API_KEY', None)

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', None)

    COHERE_API_KEY = os.getenv('COHERE_API_KEY', None)

    QDRANT_URL = os.getenv('QDRANT_URL', None)
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', None)

    CORS_ORIGIN = os.getenv('CORS_ORIGIN', None)
    
    