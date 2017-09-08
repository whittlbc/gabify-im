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

  os.system('scp {} {}'.format(source, dest))


def format_arg(instance):
  return '{}@{}:{}'.format(UBUNTU_USERNAME, instance.ip, instance.config.model_path)