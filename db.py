from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv


#Heroku
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL") 

#Venv koneella
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///suuranna"

db = SQLAlchemy(app)

