# models.py
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class Accueil(db.Model):
    __tablename__ = 'Accueil'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)

class Programme(db.Model):
    __tablename__ = 'programme'
    id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    horairePlanning = db.Column(db.Date, nullable=False)
    poste_01  = db.Column(db.String(30))
    poste_02  = db.Column(db.String(30))
    poste_03  = db.Column(db.String(30))
    poste_04  = db.Column(db.String(30))
    poste_05  = db.Column(db.String(30))
    poste_06  = db.Column(db.String(30))
    poste_07  = db.Column(db.String(30))
    poste_08  = db.Column(db.String(30))
    poste_09  = db.Column(db.String(30))
    poste_10  = db.Column(db.String(30))
    poste_11  = db.Column(db.String(30))
    poste_12  = db.Column(db.String(30))
    poste_13  = db.Column(db.String(30))
    poste_14  = db.Column(db.String(30))
    poste_15  = db.Column(db.String(30))
    poste_16  = db.Column(db.String(30))
    poste_17  = db.Column(db.String(30))
    poste_18  = db.Column(db.String(30))


    candidate_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Programme {self.datePlanning}>'