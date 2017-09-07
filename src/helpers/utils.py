import requests
import os
from urlparse import urlparse


# Get size of file in GB
def get_file_size(path):
  # Remote file
  if path.startswith('http'):
    try:
      resp = requests.head(path)

      if resp.status_code != 200:
        raise BaseException()
    except:
      raise BaseException('Error fetching remote file')

    file_size = resp.headers.get('Content-Length')

    if file_size is None:
      raise BaseException('File size couldn\'t be predetermined.')

  # Local file
  else:
    if not os.path.exists(path):
      raise BaseException('No file found at {}'.format(path))

    file_size = os.stat(path).st_size

  return int(file_size) / 1e9


# GB to GiB conversion
def gb2gib(gb):
  return 0.931323 * gb


def get_file_ext(path):
  if not path.startswith('http'):
    return path.split('.')[-1]

  parsed = urlparse(path)
  root, ext = os.path.splitext(parsed.path)

  if not ext:
    return None

  return ext[1:]