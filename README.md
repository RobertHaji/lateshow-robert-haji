# Late Show API

## Overview

The Late Show API is a Flask-based web application designed to manage episodes, guests, and their appearances on a fictional late-night show. This API allows users to interact with the data through specified endpoints.



Packages and Migrations
Database (with Sqlalchemy) Late Show Challenge 
* install `pipenv install flask flask-restful flask-sqlalchemy flask-migrate SQLAlchemy-serializer`
'flask db --help'

## Models

### Data Model

- **Episode**: Has many Guests through Appearance.
- **Guest**: Has many Episodes through Appearance.
- **Appearance**: Belongs to both Guest and Episode.

### Database Relationships

- Configure `Appearance` to cascade deletes.
- Set serialization rules to limit recursion depth.

## Validations

- The `Appearance` model must have a `rating` between 1 and 5 (inclusive).

## API Endpoints

Init migrations with `flask db init` --run only once
Create or autogenerate migrations files with `flask db migrate -m`
Apply our migrations with flask `flask db upgrade`

### Routes

## Conclusion

This API provides a robust structure for managing the Late Show's data and has been tested by Postman