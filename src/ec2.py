import boto3
import os
from src.helpers.definitions import UBUNTU_AMI_ID, FREE_INSTANCE_TYPE

region = os.environ.get('AWS_REGION_NAME')
ec2 = boto3.resource('ec2', region_name=region)


def create_instance(instance_type=FREE_INSTANCE_TYPE, tagname=''):
  instance = ec2.create_instances(
    ImageId=UBUNTU_AMI_ID,
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
    TagSpecifications=[
      {
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
    AvailabilityZone=region,
    size=size,
    VolumeType='gp2',
    TagSpecifications=[
      {
        'Tags': [
          {
            'Key': 'Name',
            'Value': tagname
          }
        ]
      }
    ]
  )