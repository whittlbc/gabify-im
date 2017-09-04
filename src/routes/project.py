import os
import math
import yaml
from flask_restplus import Resource
from src import dbi
from src.models import Project
from src.routes import namespace, api
from src.helpers.definitions import tmp_dir, GAB_FILE
from src.helpers.utils import get_file_size, gb2gib
from src.ec2 import create_instance, create_volume


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

    tmp_repo_dir = tmp_dir + '/repo'

    # git clone the repo locally to access some of its files
    os.system('git clone {} {}'.format(repo, tmp_repo_dir))

    # Get it's .gab.yml file
    with open('{}/{}'.format(tmp_repo_dir, GAB_FILE)) as f:
      config = yaml.load(f)

    # Figure out which size of volume you'll need to create to hold the dataset
    dataset_loc = config['dataset']['location']
    dataset_size = gb2gib(get_file_size(dataset_loc))  # in GiB
    vol_size = int(math.ceil(dataset_size)) + 1  # adding extra GiB in volume

    # Create ec2 volume to hold the dataset
    create_volume(vol_size, project.uid)

    # Create ec2 instance for the API
    create_instance('API-{}'.format(project.uid))

    # Start a watcher for the instance to check when it's available

    return '', 200