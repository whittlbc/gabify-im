"""
Create a new Gabify project and everything that goes along with the initial setup
"""
import os
import math
from src import dbi
from src.models import Project
from src.helpers.definitions import tmp_dir, GAB_FILE, API_AMI_ID, VOLUME_DEVICE
from src.services import config_from_file, create_volume, create_instance, watch_instance_until_running, init_attached_volume
from src.helpers.utils import get_file_size, gb2gib
from src.helpers import roles


# TODO: Run this whole thing as a transaction
def perform(repo):
  # Create new Project for repo
  project = dbi.create(Project, {'repo': repo})

  # Clone the repo locally to access its files
  tmp_repo_dir = '{}/{}'.format(tmp_dir, project.uid)
  os.system('git clone {} {}'.format(repo, tmp_repo_dir))

  # Get a Config model instance from the project's .gab.yml file
  config_path = '{}/{}'.format(tmp_repo_dir, GAB_FILE)
  config = config_from_file.perform(config_path, project)

  # Figure out which size volume you will need to hold the dataset
  dataset_size = gb2gib(get_file_size(config.dataset_loc))  # in GiB
  vol_size = int(math.ceil(dataset_size)) + 1  # adding extra GiB in volume

  # Create EC2 Volume and DB representation
  volume = create_volume.perform(project, vol_size)

  # Create EC2 API Instance and DB representation
  instance = create_instance.perform(project, image_id=API_AMI_ID, role=roles.API)

  # Wait until instance is running
  aws_instance = watch_instance_until_running.perform(instance)

  # Update instance's IP
  instance = dbi.update(instance, {'ip': aws_instance.public_ip_address})

  # Attach Volume to API Instance
  aws_instance.attach_volume(
    Device=VOLUME_DEVICE,
    VolumeId=volume.aws_volume_id
  )

  # Initialize the newly attached volume on the instance
  init_attached_volume.perform(instance, config)

  # Detach the volume
  aws_instance.detach_volume(
    Device=VOLUME_DEVICE,
    VolumeId=volume.aws_volume_id,
    Force=False
  )