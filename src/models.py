"""
Declare your database tables as model representations
"""
from src import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
from uuid import uuid4


class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(120), index=True, unique=True, nullable=False)
  repo = db.Column(db.String(240))
  config = db.relationship('Config', uselist=False, back_populates='project')
  volume = db.relationship('Volume', uselist=False, back_populates='project')
  is_destroyed = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, repo=None):
    self.uid = uuid4().get_hex()
    self.repo = repo

  def __repr__(self):
    return '<Project id={}, uid={}, repo={}, is_destroyed={}, created_at={}>'.format(
      self.id, self.uid, self.repo, self.is_destroyed, self.created_at)


class Volume(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  aws_volume_id = db.Column(db.String(120), unique=True, nullable=False)
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True, nullable=False)
  project = db.relationship('Project', back_populates='volume')
  size = db.Column(db.Integer)
  is_destroyed = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, aws_volume_id=None, project=None, size=0):
    self.aws_volume_id = aws_volume_id
    self.project = project
    self.size = size

  def __repr__(self):
    return '<Volume id={}, aws_volume_id={}, project_id={}, size={}, is_destroyed={}, created_at={}>'.format(
      self.id, self.aws_volume_id, self.project_id, self.size, self.is_destroyed, self.created_at)


class Instance(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  aws_instance_id = db.Column(db.String(120), unique=True, nullable=False)
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True, nullable=False)
  project = db.relationship('Project', backref='instances')
  instance_type = db.Column(db.String(120))
  role = db.Column(db.Integer, nullable=False)
  ip = db.Column(db.String(120))
  is_destroyed = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, aws_instance_id=None, project=None, instance_type=None, role=None):
    self.aws_instance_id = aws_instance_id
    self.project = project
    self.instance_type = instance_type
    self.role = role

  def __repr__(self):
    return '<Instance id={}, aws_instance_id={}, project_id={}, instance_type={}, role={}, ip={}, is_destroyed={}, created_at={}>'.format(
      self.id, self.aws_instance_id, self.project_id, self.instance_type, self.role, self.ip, self.is_destroyed, self.created_at)

"""
dataset:
  location: https://s3-us-west-1.amazonaws.com/jarvisdev/glimpse/dataset-100.hdf5
  update_with: src.dataset.update
  retrain_after: 100

model: data/model.ckpt

train:
- python train.py

test:
- python test.py

predict: src.model.predict
"""

class Config(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'), index=True, nullable=False)
  project = db.relationship('Project', back_populates='config')
  dataset_loc = db.Column(db.String(240))
  update_with = db.Column(db.String(120))
  retrain_after = db.Column(db.Integer)
  model_path = db.Column(db.String(240))
  train = db.Column(JSON, default=[])
  test = db.Column(JSON, default=[])
  predict = db.Column(db.String(120))

  def __init__(self, project, config={}):
    self.project = project

    # Make sure the required fields are provided
    dataset = config.get('dataset')
    assert dataset

    dataset_loc = dataset.get('location')
    assert dataset_loc

    model_path = config.get('model')
    assert model_path

    train = config.get('train')
    assert train

    predict = config.get('predict')
    assert predict

    # Set all config-related attrs
    self.dataset_loc = dataset_loc
    self.update_with = dataset.get('update_with')
    self.retrain_after = dataset.get('retrain_after')
    self.model_path = model_path
    self.train = train
    self.test = config.get('test')
    self.predict = predict

  def __repr__(self):
    return '<Config id={}, project_id={}, dataset_loc={}, update_with={}, retrain_after={}, model_path={}, train={}, test={}, predict={}>'.format(
      self.id, self.project_id, self.dataset_loc, self.update_with, self.retrain_after, self.model_path, self.train, self.test, self.predict)