from flask_restplus import Resource
from src import dbi
from src.models import Project
from src.routes import namespace, api


@namespace.route('/projects')
class CreateUser(Resource):
  """Lets you POST to create a new project"""

  @namespace.doc('create_project')
  def post(self):
    # email = api.payload['email']
    # hashed_pw = None
    #
    # # Find the school they selected
    # school = dbi.find_one(School, {'slug': api.payload['school']})
    #
    # user_validation_error = user_validation.validate_user(email, school)
    #
    # # Return user-validation error if one exists
    # if user_validation_error:
    #   return dict(error=user_validation_error), 400
    #
    # # Password still optional at this point
    # if 'password' in api.payload:
    #   hashed_pw = auth_util.hash_pw(api.payload['password'])
    #
    # user = dbi.find_one(User, {'email': email})
    #
    # # If user doesn't exist yet, create him
    # if not user:
    #   dbi.create(User, {
    #     'email': email,
    #     'name': api.payload['name'],
    #     'school': school,
    #     'hashed_pw': hashed_pw
    #   })

    return '', 201