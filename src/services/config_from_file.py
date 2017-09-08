import yaml
from src.models import Config
from src.dbi import create
from src import logger


def perform(path, project):
  logger.info('Reading config...')

  with open(path) as f:
    config_yaml = yaml.load(f)

  return create(Config, {
    'project': project,
    'config': config_yaml
  })