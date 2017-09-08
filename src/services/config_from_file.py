import yaml
from src.models import Config
from src.dbi import create


def perform(path, project):
  with open(path) as f:
    config_yaml = yaml.load(f)

  return create(Config, {
    'project': project,
    'config': config_yaml
  })