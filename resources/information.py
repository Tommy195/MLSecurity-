from flask_restful import Resource
from app.models.information import InformationModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger

class Information(Resource):

    def __init__(self):
        self.logger = create_logger()

    @jwt_required() 
    def get(self):
        try:
            information = InformationModel.get(self)
            return {'message': 'Information fetched correctly'}, 200
        except:
            return {'message': 'Could not retrieve information from endpoint or endpoint was not available'}, 404

    @jwt_required() 
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}
        
class InformationList(Resource):
    
    @jwt_required()
    def get(self):
        return {'information': [information.json() for information in information.query.all()]}

class InformationById(Resource):
    
    @jwt_required() 
    def find_by_id(self, id):
        information = information.find_by_name(name)
        if information:
            return information.json()
        return {'message': 'Store not found'}, 404    