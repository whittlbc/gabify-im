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


def is_instance_running(aws_instance_id):
  aws_instance = ec2.Instance(aws_instance_id)

  try:
    state = aws_instance.state or {}
  except BaseException, e:
    logger.error('Error finding state of instance by aws id, {}, with error: {}'.format(aws_instance_id, e))
    return False

  return aws_instance, state.get('Code') == 16