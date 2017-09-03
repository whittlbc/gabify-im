"""
  API for model predictions and updating of dataset
"""
import importlib
import os
import yaml
import json
from inspect import getargspec
from flask import Flask, request, make_response

GAB_FILE = '<GAB_FILE>'
APP_NAME = '<APP_NAME>'

if not os.path.exists(GAB_FILE):
  raise BaseException('No .gab.yml file found.')

with open(GAB_FILE) as f:
  config = yaml.load(f)

if type(config) != dict or not config.get('predict'):
  raise BaseException('Invalid .gab.yml file')

split_path_info = config.get('predict').split('.')

predict_func_str = split_path_info.pop()
predict_mod_str = '.'.join(split_path_info)

if not predict_mod_str:
  raise BaseException('No module specified for making predictions. Only the function was specified.')

# Get reference to predict module
predict_mod = importlib.import_module(predict_mod_str)

if not predict_mod:
  raise BaseException('No module to import at destination: {}'.format(predict_mod_str))

if not hasattr(predict_mod, predict_func_str):
  raise BaseException('No function named {} exists on module {}'.format(predict_func_str, predict_mod_str))

predict = getattr(predict_mod, predict_func_str)
predict_args = getargspec(predict).args

# Create new Flask app
app = Flask(__name__)


@app.route('/{}/predict'.format(APP_NAME))
def get_prediction():
  request_args = dict(request.args.items())

  # Only let supported named parameters through
  valid_args = {k: v for k, v in request_args.iteritems() if k in predict_args}

  prediction = None
  error = None

  try:
    prediction = predict(**valid_args)
  except BaseException, e:
    error = 'Prediction Error, {}'.format(e.message)

  if not prediction and not error:
    error = 'No prediction result to return :/'

  if error:
    payload = {'error': error}
  else:
    payload = {'prediction': prediction}

  resp = make_response(json.dumps(payload))
  resp.headers['content-type'] = 'application/json'

  return resp, 200


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)