from flask_restful import Resource
from model import Episode


class EpisodeResource(Resource):
    def get(self, id=None):
        if id is None:
            episodes = Episode.query.all()  # Query all powers from the database
            return [
                episode.to_dict() for episode in episodes
            ], 200  # Return serialized list of powers with a 200 status code
        else:
            episode = Episode.query.filter_by(id=id).first()

            if episode is None:
                return {"message": "Episode not found"}, 404
            return episode.to_dict()
