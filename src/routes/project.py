import os
import math
import yaml
from flask_restplus import Resource
from src import dbi, logger
from src.models import Project, Volume, Instance, Config
from src.routes import namespace, api
from src.helpers.definitions import tmp_dir, GAB_FILE, FREE_INSTANCE_TYPE, API_AMI_ID
from src.helpers.utils import get_file_size, gb2gib, get_file_ext
from src.ec2 import create_instance, create_volume
from src.helpers import roles
from src.services import watch_instance_until_running
from src.ssh import remote_exec


@namespace.route('/projects')
class CreateUser(Resource):
  """Lets you POST to create a new project"""

  @namespace.doc('create_project')
  def post(self):
    # Get the repo url they passed in
    # repo = api.payload['repo']
    repo = 'https://github.com/whittlbc/gabify-ex-proj.git'

    # Create a new Project model for them
    project = dbi.create(Project, {'repo': repo})

    # Create a delayed job to handle all of the below, and if anything ever goes wrong, destroy the project

    tmp_repo_dir = '{}/{}'.format(tmp_dir, project.uid)

    # git clone the repo locally to access some of its files
    os.system('git clone {} {}'.format(repo, tmp_repo_dir))

    # Get it's .gab.yml file
    with open('{}/{}'.format(tmp_repo_dir, GAB_FILE)) as f:
      config_yaml = yaml.load(f)

    try:
      config = dbi.create(Config, {'project': project, 'config': config_yaml})
    except AssertionError:
      logger.error('Invalid config file')
      return 'Invalid config file', 500

    # Figure out which size of volume you will need to hold the dataset
    dataset_size = gb2gib(get_file_size(config.dataset_loc))  # in GiB
    vol_size = int(math.ceil(dataset_size)) + 1  # adding extra GiB in volume

    # Get the file extension for the dataset
    dataset_ext = get_file_ext(config.dataset_loc)

    try:
      # Create ec2 volume to hold the dataset
      aws_volume = create_volume(size=vol_size, tagname=project.uid)

      volume = dbi.create(Volume, {
        'aws_volume_id': aws_volume.id,
        'project': project,
        'size': aws_volume.size
      })
    except BaseException, e:
      logger.error('Error Creating Volume: {}'.format(e))
      return 'Error Creating Volume', 500

    try:
      # Create ec2 instance for the API
      aws_instance = create_instance(image_id=API_AMI_ID, tagname='API-{}'.format(project.uid))

      instance = dbi.create(Instance, {
        'aws_instance_id': aws_instance.id,
        'project': project,
        'instance_type': FREE_INSTANCE_TYPE,
        'role': roles.API
      })
    except BaseException, e:
      logger.error('Error creating API instance: {}'.format(e))
      return 'Error Creating Instance', 500

    # Wait until instance is running
    aws_instance = watch_instance_until_running.perform(instance)

    # Update instance's IP
    instance = dbi.update(instance, {'ip': aws_instance.public_ip_address})

    try:
      aws_instance.attach_volume(
        Device='/dev/sdh',
        VolumeId=volume.aws_volume_id
      )
    except BaseException, e:
      logger.error('Error attaching volume({}) to instance({}): {}'.format(
        volume.aws_volume_id, aws_instance.id, e))

      return 'Error Attaching Volume', 500

    remote_exec(instance.ip, 'init_attached_vol', sudo=True)
    remote_exec(instance.ip, 'init_vol', sudo=True)
    remote_exec(instance.ip, 'mount_dsetvol', sudo=True)
    remote_exec(instance.ip, 'wget -O /dsetvol/dataset.{} {}'.format(dataset_ext, config.dataset_loc))
    remote_exec(instance.ip, 'unmount_dsetvol', sudo=True)

    aws_instance.detach_volume(
      Device='/dev/sdh',
      VolumeId=volume.aws_volume_id,
      Force=False
    )

    return '', 200