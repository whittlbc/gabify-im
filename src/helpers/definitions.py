import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
tmp_dir = base_dir + '/tmp'

GAB_FILE = '.gab.yml'
UBUNTU_AMI_ID = 'ami-cd0f5cb6'
FREE_INSTANCE_TYPE = 't2.micro'
GPU_INSTANCE_TYPE = 'p2.xlarge'