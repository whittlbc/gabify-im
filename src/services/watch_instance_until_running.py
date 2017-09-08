"""
Poll the AWS API until a certain instance is 'running'
"""
from src.ec2 import is_instance_running
from time import sleep
from src import logger


def perform(instance, interval=10):
  logger.info('Watching instance until running...')

  running = False
  while not running:
    aws_instance, running = is_instance_running(instance.aws_instance_id)
    sleep(interval)

  return aws_instance