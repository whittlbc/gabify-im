from src.ec2 import is_instance_running
from time import sleep
from src.dbi import update


class WatchInstanceUntilRunning:
  CHECK_INTERVAL = 10

  def __init__(self, instance, on_done=None):
    self.instance = instance
    self.on_done = on_done

  def perform(self):
    running = False

    # Keep checking on the instance until it's running
    while not running:
      aws_instance, running = is_instance_running(self.instance.aws_instance_id)
      if not running: sleep(self.CHECK_INTERVAL)

    # Once it's running, update the IP address of the DB instance
    update(self.instance, {'ip': aws_instance.public_ip_address})

    if self.on_done:
      self.on_done(self.instance)