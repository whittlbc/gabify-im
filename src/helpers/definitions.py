import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
tmp_dir = base_dir + '/tmp'
pem_key = base_dir + '/gabify-norcal.pem'

GAB_FILE = '.gab.yml'
UBUNTU_AMI_ID = 'ami-09d2fb69'
API_AMI_ID = 'ami-5d37003d'
TRAINER_AMI_ID = 'ami-5d37003d'
FREE_INSTANCE_TYPE = 't2.micro'
GPU_INSTANCE_TYPE = 'p2.xlarge'
UBUNTU_USERNAME = 'ubuntu'
VOLUME_DEVICE = '/dev/sdh'