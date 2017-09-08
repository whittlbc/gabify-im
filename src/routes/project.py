from flask_restplus import Resource, fields
from src import delayed, dbi
from src.routes import namespace, api
from src.services import create_project, train_model
from src.models import Project

create_project_model = api.model('Project', {
  'repo': fields.String(required=True)
})

train_project_model = api.model('Project', {
  'uid': fields.String(required=True)
})


@namespace.route('/projects')
class CreateProject(Resource):
  @namespace.doc('create_project')
  @namespace.expect(create_project_model, validate=True)
  def post(self):
    # Get project repository url
    repo = api.payload['repo']

    # Schedule a create_new_project service
    delayed.add_job(create_project.perform, args=[repo])

    return '', 200


@namespace.route('/train')
class TrainProject(Resource):
  @namespace.doc('train_project')
  @namespace.expect(train_project_model, validate=True)
  def post(self):
    # Attempt to find the project by uid
    project_uid = api.payload['uid']
    project = dbi.find_one(Project, {'uid': project_uid})

    if not project:
      return 'No Project for uid: {}'.format(project_uid), 404

    if not project.train:
      return 'No train commands configured yet.', 500

    # Schedule a train_model service for this project
    delayed.add_job(train_model.perform, args=[project])

    return '', 200
