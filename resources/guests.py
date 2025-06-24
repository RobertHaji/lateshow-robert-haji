from flask_restful import Resource
from model import Guest


class GuestResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return [guest.to_dict() for guest in guests], 200
