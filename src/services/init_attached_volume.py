from src.helpers.utils import get_file_ext
from src.ssh import remote_exec


def perform(instance, config=None):
  config = config or instance.config
  dataset_loc = config.dataset_loc

  remote_exec(instance.ip, 'init_attached_vol', sudo=True)
  remote_exec(instance.ip, 'init_vol', sudo=True)
  remote_exec(instance.ip, 'mount_dsetvol', sudo=True)
  remote_exec(instance.ip, 'wget -O /dsetvol/dataset.{} {}'.format(get_file_ext(dataset_loc), dataset_loc), sudo=True)
  remote_exec(instance.ip, 'unmount_dsetvol', sudo=True)
