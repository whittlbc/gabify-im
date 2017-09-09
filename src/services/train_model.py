"""
Train a model and transfer that model to the project's API instance afterwards
"""
from src.services import create_instance, watch_instance_until_running, transfer_model
from src import dbi, logger
from src.helpers import roles
from src.helpers.definitions import TRAINER_AMI_ID, VOLUME_DEVICE
from src.models import Instance
from src.ssh import remote_exec
from src.ec2 import ec2


def perform(project):
  # Get the trainer instance for this project
  instance = dbi.find_one(Instance, {'project': project, 'role': roles.TRAINER})

  if instance:
    aws_instance = ec2.Instance(instance.aws_instance_id)
  else:
    # Create instance if not there
    instance = create_instance.perform(project, image_id=TRAINER_AMI_ID, role=roles.TRAINER)

    # Wait for it to start running...
    aws_instance = watch_instance_until_running.perform(instance)

    logger.info('Setting instance\'s IP...')

    # Update the IP
    instance = dbi.update(instance, {'ip': aws_instance.public_ip_address})

  logger.info('Attaching volume to trainer instance...')

  # TODO: Not sure what error we'll run into if the volume is already attached...check for this
  # Attach volume to trainer instance
  aws_instance.attach_volume(
    Device=VOLUME_DEVICE,
    VolumeId=project.volume.aws_volume_id
  )

  out, err = remote_exec(instance.ip, 'ls -l /usr/local/bin | grep init_vol')

  # if init_vol script doesn't exist yet, run init_attached_vol
  if not out:
    remote_exec(instance.ip, 'init_attached_vol', sudo=True)
  # TODO: Might run into error with this one if it's already been run...might need to check if /dsetvol exists
  remote_exec(instance.ip, 'init_vol', sudo=True)
  remote_exec(instance.ip, 'mount_dsetvol', sudo=True)

  # The code needs to be put on instance first...
  # ...also tensorflow-gpu should be pip installed (while inside virtualenv)

  # Run train command(s) on trainer instance
  for cmd in project.config.train:
    remote_exec(instance.ip, cmd)

  # Move model from trainer instance to API instance
  api_instance = dbi.find_one(Instance, {'project': project, 'role': roles.API})
  transfer_model.perform(instance, api_instance)

  logger.info('Stopping trainer instance...')

  # Spin down instance
  instance.stop()