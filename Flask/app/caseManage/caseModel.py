from app import db

class EarthquakeCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    occurrence_time = db.Column(db.Boolean)
    magnitude = db.Column(db.Float)
    intensity = db.Column(db.Integer)
    population_density = db.Column(db.Float)
    earthquake_forecast = db.Column(db.Boolean)
    death_rate = db.Column(db.Float)
    injury_rate = db.Column(db.Float)