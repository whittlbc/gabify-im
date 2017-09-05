import os
import math
import yaml
from flask_restplus import Resource
from src import dbi, logger
from src.models import Project, Volume, Instance
from src.routes import namespace, api
from src.helpers.definitions import tmp_dir, GAB_FILE, FREE_INSTANCE_TYPE, API_AMI_ID
from src.helpers.utils import get_file_size, gb2gib
from src.ec2 import create_instance, create_volume
from src.helpers import roles


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

    tmp_repo_dir = '{}/{}'.format(tmp_dir, project.uid)

    # git clone the repo locally to access some of its files
    os.system('git clone {} {}'.format(repo, tmp_repo_dir))

    # Get it's .gab.yml file
    with open('{}/{}'.format(tmp_repo_dir, GAB_FILE)) as f:
      config = yaml.load(f)

    # Figure out which size of volume you will need to hold the dataset
    dataset_loc = config['dataset']['location']
    dataset_size = gb2gib(get_file_size(dataset_loc))  # in GiB
    vol_size = int(math.ceil(dataset_size)) + 1  # adding extra GiB in volume

    try:
      # Create ec2 volume to hold the dataset
      volume = create_volume(size=vol_size, tagname=project.uid)

      dbi.create(Volume, {
        'aws_volume_id': volume.id,
        'project': project,
        'size': volume.size
      })
    except BaseException, e:
      logger.error('Error Creating Volume: {}'.format(e))
      return 'Error Creating Volume', 500

    try:
      # Create ec2 instance for the API
      api_instance = create_instance(image_id=API_AMI_ID, tagname='API-{}'.format(project.uid))

      dbi.create(Instance, {
        'aws_instance_id': api_instance.id,
        'project': project,
        'instance_type': FREE_INSTANCE_TYPE,
        'role': roles.API
      })
    except BaseException, e:
      logger.error('Error creating API instance: {}'.format(e))
      return 'Error Creating Instance', 500

    # Start a watcher for the instance to check when it's available...

    # Once it's available:
    #
    # (1) store IP address in api_instance.ip
    # (2) attach volume to api_instance
    # (3) ssh into api_instance
    # - these bash scripts should just be an image snapshot <-- WRONG, WRITE ONE BASH SCRIPT THAT GIT CLONES A REPO CONTAINING THESE BASH SCRIPTS INSTEAD. YOU DON'T WANT YOUR IMAGE HAVING TO BE UPDATED
    # (4) init_new_vol
    # (5) mount_dsetvol
    # (6) download dataset onto new volume
    # (7) unmount dsetvol
    # (8) detach volume from api_instance



    return '', 200