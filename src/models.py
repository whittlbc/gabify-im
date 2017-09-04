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

  def __init__(self, repo):
    self.uid = uuid4().get_hex()
    self.repo = repo

  def __repr__(self):
    return '<User id={}, uid={}, repo={}, is_destroyed={}, created_at={}>'.format(
      self.id, self.uid, self.repo, self.is_destroyed, self.created_at)