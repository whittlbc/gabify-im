import os
from src.helpers.env import env


class Config:
  DEBUG = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProdConfig(Config):
  DEBUG = False


class DevConfig(Config):
  def __init__(self):
    pass


class TestConfig(Config):
  def __init__(self):
    pass


def get_config():
  config_class = globals().get('{}Config'.format(env().capitalize()))
  return config_class()