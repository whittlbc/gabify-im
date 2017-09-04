from flask_restplus import Resource
from src import dbi
from src.models import Project
from src.routes import namespace, api


@namespace.route('/projects')
class CreateUser(Resource):
  """Lets you POST to create a new project"""

  @namespace.doc('create_project')
  def post(self):
    # repo = api.payload['repo']
    repo = 'https://github.com/whittlbc/gabify_ex_proj.git'

    project = dbi.create(Project, {'repo': repo})

    # Do all the init shit

    return '', 200