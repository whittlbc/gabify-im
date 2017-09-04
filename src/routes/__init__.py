from flask_restplus import Api

api = Api(version='0.1', title='Gabify API')
namespace = api.namespace('api')

# Add all route handlers here:
from src.routes.project import *