from src.ec2 import is_instance_running
from time import sleep


def perform(instance, interval=10):
  running = False

  while not running:
    aws_instance, running = is_instance_running(instance.aws_instance_id)
    if not running: sleep(interval)

  return aws_instance