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

  # Attach volume to trainer instance (if not already attached)
  attached_vol_ids = [v.id for v in aws_instance.volumes.all()]
  project_vol_id = project.volume.aws_volume_id

  if project_vol_id not in attached_vol_ids:
    logger.info('Attaching volume to trainer instance...')

    aws_instance.attach_volume(
      Device=VOLUME_DEVICE,
      VolumeId=project_vol_id
    )

  out, err = remote_exec(instance.ip, 'ls -l /usr/local/bin | grep init_vol')

  # if init_vol script doesn't exist yet, run init_attached_vol
  if not out:
    remote_exec(instance.ip, 'init_attached_vol', sudo=True)

  # Run the rest of the volume initialization scripts
  remote_exec(instance.ip, 'yes Yes | sudo init_vol')
  remote_exec(instance.ip, 'mount_dsetvol', sudo=True)

  out, err = remote_exec(instance.ip, 'ls -l | grep {}'.format(project.uid))

  # Clone the project onto the instance if not already there
  if not out:
    remote_exec(instance.ip, 'git clone {}.git {}'.format(project.repo, project.uid))

    # Add the files to the project that you need:
    # api.py and watcher.py

    # Add/update config vars for project (however you plan to go about doing this)

    # Remove tensorflow or tensorflow-gpu from requirements.txt if there

    remote_exec(instance.ip, 'cd {} && source venv/bin/activate && pip install -r requirements.txt && pip install tensorflow-gpu'.format(project.uid))

  # Run train command(s) on trainer instance
  for cmd in project.config.train:
    remote_exec(instance.ip, cmd)

  # Move model from trainer instance to API instance
  api_instance = dbi.find_one(Instance, {'project': project, 'role': roles.API})
  transfer_model.perform(instance, api_instance)

  logger.info('Stopping trainer instance...')

  # Spin down instance
  instance.stop()