"""
Declare your database tables as model representations
"""
from src import db
import datetime
from uuid import uuid4


class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uid = db.Column(db.String(120), index=True, unique=True, nullable=False)
  repo = db.Column(db.String(240))
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
  project = db.relationship('Project', backref='volume')
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
  is_destroyed = db.Column(db.Boolean(), default=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def __init__(self, aws_instance_id=None, project=None, instance_type=None, role=None):
    self.aws_instance_id = aws_instance_id
    self.project = project
    self.instance_type = instance_type
    self.role = role

  def __repr__(self):
    return '<Instance id={}, aws_instance_id={}, project_id={}, is_destroyed={}, created_at={}>'.format(
      self.id, self.aws_instance_id, self.project_id, self.instance_type, self.is_destroyed, self.created_at)