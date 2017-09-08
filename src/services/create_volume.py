from src import ec2, logger
from src.dbi import create
from src.models import Volume


def perform(project, size):
  logger.info('Creating volume...')

  # Create ec2 volume to hold the dataset
  aws_volume = ec2.create_volume(size=size, tagname=project.uid)

  return create(Volume, {
    'aws_volume_id': aws_volume.id,
    'project': project,
    'size': aws_volume.size
  })