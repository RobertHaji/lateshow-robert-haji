from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from model import db
from resources.episodes import EpisodeResource

# Initialize the Flask Application

app = Flask(__name__)

# Then Config the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///episodes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and the migrations

db.init_app(app)
migrate = Migrate(app, db)

# link flask-restful with flask
api = Api(app)

# Routes

# Get all episodes and by the Id
api.add_resource(EpisodeResource, "/episodes", "/episodes/<int:id>")


if __name__ == "__main__":
    app.run(port=5555)