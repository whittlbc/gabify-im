import boto3
import os
from src.helpers.definitions import UBUNTU_AMI_ID, FREE_INSTANCE_TYPE

region_name = os.environ.get('AWS_REGION_NAME')
zone_name = os.environ.get('AWS_ZONE_NAME')

ec2 = boto3.resource('ec2', region_name=region_name)


def create_instance(instance_type=FREE_INSTANCE_TYPE, tagname=''):
  instance = ec2.create_instances(
    ImageId=UBUNTU_AMI_ID,
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
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