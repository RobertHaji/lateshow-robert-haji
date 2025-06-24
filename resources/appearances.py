from flask_restful import Resource
from flask import request
from model import Appearance, Episode, Guest, db

class AppearanceResource(Resource):
    def post(self):
        data = request.get_json() #get json data from the request

        # Validate our request body
        required_fields = ["rating", "episode_id", "guest_id"]
        if not all(field in data for field in required_fields):
            return {"errors": ["validation errors"]}, 400  # Bad Request

        # Fetch the related episode and guest
        episode = Episode.query.filter_by(id=data["episode_id"]).first()
        guest = Guest.query.filter_by(id=data["guest_id"]).first()

        if not episode or not guest:
            return {"errors": ["validation errors"]}, 400  # Bad Request

        # Create a new Appearance instance
        appearance = Appearance(
            rating=data["rating"],
            episode_id=data["episode_id"],
            guest_id=data["guest_id"],
        )

        db.session.add(appearance)  # Add the new Appearance to the session
        db.session.commit()  # Commit the session to save the changes in our database

        # Return the newly created Appearance data
        return {
            "id": appearance.id,
            "rating": appearance.rating,
            "guest_id": appearance.guest_id,
            "episode_id": appearance.episode_id,
            "episode": {
                "id": episode.id,
                "date": episode.date,
                "number": episode.number,
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation,
            },
        }, 201  # 201 Created