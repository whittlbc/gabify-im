import boto3
import os
from src import logger
from src.helpers.definitions import UBUNTU_AMI_ID, FREE_INSTANCE_TYPE

region_name = os.environ.get('AWS_REGION_NAME')
zone_name = os.environ.get('AWS_ZONE_NAME')
key_pair_name = os.environ.get('KEY_PAIR_NAME')
ssh_security_group = os.environ.get('SSH_SECURITY_GROUP_ID')

ec2 = boto3.resource('ec2', region_name=region_name)


def create_instance(instance_type=FREE_INSTANCE_TYPE, image_id=UBUNTU_AMI_ID, tagname=''):
  instance = ec2.create_instances(
    ImageId=image_id,
    MinCount=1,
    MaxCount=1,
    KeyName=key_pair_name,
    InstanceType=instance_type,
    SecurityGroupIds=[
      ssh_security_group
    ],
    Placement={
      'AvailabilityZone': zone_name
    },
    TagSpecifications=[
      {
        'ResourceType': 'instance',
        'Tags': [
          {
            'Key': 'Name',
            'Value': tagname
          }
        ]
      }
    ]
  )

  return instance[0]


def create_volume(size=1, tagname=''):
  return ec2.create_volume(
    AvailabilityZone=zone_name,
    Size=size,
    VolumeType='gp2',
    TagSpecifications=[
      {
        'ResourceType': 'volume',
        'Tags': [
          {
            'Key': 'Name',
            'Value': tagname
          }
        ]
      }
    ]
  )


def is_instance_running(instance_id):
  try:
    instances = ec2.instances.filter(InstanceIds=[instance_id])
    instances = list(instances)
  except BaseException, e:
    logger.error('Error finding instance by id, {}, with error: {}'.format(instance_id, e))
    return False

  if not instances:
    return False

  return instances[0].state.get('Code') == 16