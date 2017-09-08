from paramiko import SSHClient, AutoAddPolicy
from src.helpers.definitions import UBUNTU_USERNAME, pem_key
from src import logger

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())


def remote_exec(ip, cmd, sudo=False, log=True):
  if sudo:
    cmd = 'sudo ' + cmd

  try:
    ssh.connect(ip, username=UBUNTU_USERNAME, key_filename=pem_key)
  except BaseException:
    raise BaseException('Connecting to host {} failed.'.format(ip))

  try:
    if log:
      logger.info('Running {} on {}'.format(cmd, ip))

    stdin, stdout, stderr = ssh.exec_command(cmd)
  except BaseException:
    raise BaseException('Error running {} on {}'.format(cmd, ip))

  return stdout.read()