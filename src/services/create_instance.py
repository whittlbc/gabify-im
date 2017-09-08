from src.dbi import create
from src.models import Instance
from src import ec2, logger
from src.helpers.definitions import FREE_INSTANCE_TYPE


def perform(project, instance_type=FREE_INSTANCE_TYPE, image_id=None, role=None):
  logger.info('Creating {} instance...'.format(instance_type))

  aws_instance = ec2.create_instance(
    instance_type=instance_type,
    image_id=image_id,
    tagname=ec2.instance_tagname(project)
  )

  return create(Instance, {
    'aws_instance_id': aws_instance.id,
    'project': project,
    'instance_type': instance_type,
    'role': role
  })