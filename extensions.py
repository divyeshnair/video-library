from flask_sqlalchemy import SQLAlchemy

session = SQLAlchemy()
db = session.session
Model = session.Model