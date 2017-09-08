from flask_restplus import Resource, fields
from src import delayed
from src.routes import namespace, api
from src.services import create_project

create_project_model = api.model('Project', {
  'repo': fields.String(required=True)
})


@namespace.route('/projects')
class CreateUser(Resource):
  """Lets you POST to create a new project"""

  @namespace.doc('create_project')
  @namespace.expect(create_project_model, validate=True)
  def post(self):
    # Get project repository url
    repo = api.payload['repo']

    # Schedule a create_new_project service
    delayed.add_job(create_project.perform, args=[repo])

    return '', 200