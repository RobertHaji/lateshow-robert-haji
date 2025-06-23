from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# 1. Defines naming convention
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# 2. Create a metadata object with the naming convention
metadata = MetaData(naming_convention=convention)

# Initialize SQLAlchemy with the metadata
db = SQLAlchemy(metadata=metadata)


class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    serialize_rules = ("-appearances.episode",)  # This prevents recursion

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship(
        "Appearance", back_populates="episode", cascade="all, delete-orphan"
    )


class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    serialize_rules = ("-appearances.guest",)  # This prevents recursion

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    occupation = db.Column(db.String(50))

    appearances = db.relationship(
        "Appearance", back_populates="guest", cascade="all, delete-orphan"
    )


class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    serialize_rules = (
        "-guest.appearances",
        "-episode.appearances",
    )  # This prevents recursion

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    # Add validation logic to our Appearance i.e the rating
    @db.validates("rating")
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5 (inclusive).")
        return rating