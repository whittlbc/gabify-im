import boto3
import os
from src.helpers.definitions import UBUNTU_AMI_ID, FREE_INSTANCE_TYPE

ec2 = boto3.resource('ec2', region_name=os.environ.get('AWS_REGION_NAME'))


def create_instance(image_id=UBUNTU_AMI_ID, instance_type=FREE_INSTANCE_TYPE):
  instance = ec2.create_instances(
    ImageId=image_id,
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type)

  return instance[0]