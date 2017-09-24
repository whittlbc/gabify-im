"""
Transfer model between Trainer/API instances for a project
"""
import os
from src import logger
from src.helpers.definitions import UBUNTU_USERNAME


def perform(from_instance, to_instance):
  source = format_arg(from_instance)
  dest = format_arg(to_instance)

  logger.info('Transferring model from {} to {}'.format(source, dest))

  # TODO: Don't think this will work...will need to do 2 separate transfers
  # with a cache dir in this project as location #2
  os.system('scp {} {}'.format(source, dest))


def format_arg(instance):
  return '{}@{}:{}'.format(UBUNTU_USERNAME, instance.ip, instance.config.model_path)