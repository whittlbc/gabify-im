from paramiko import SSHClient, AutoAddPolicy
from src.helpers.definitions import UBUNTU_USERNAME, pem_key

ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())


def remote_exec(ip, cmd, sudo=False):
  if sudo:
    cmd = 'sudo ' + cmd

  try:
    ssh.connect(ip, username=UBUNTU_USERNAME, key_filename=pem_key)
  except BaseException:
    raise BaseException('Connecting to host {} failed.'.format(ip))

  try:
    stdin, stdout, stderr = ssh.exec_command(cmd)
  except BaseException:
    raise BaseException('Error running {} on {}'.format(cmd, ip))

  err = stderr.read()

  if err:
    raise BaseException('Error running {} on {}: {}'.format(cmd, ip, err))

  return stdout.read()