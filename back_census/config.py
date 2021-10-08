import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    CENSUS_KEY = os.environ.get('CENSUS_KEY')
