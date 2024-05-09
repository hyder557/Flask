from app import db

class Demand(db.Model):
    __tablename__ = 'demands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    resources = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="处理中")
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
	    return {
		    'id': self.id,
		    'name': self.name,
		    'contact': self.contact,
		    'location': self.location,
		    'description': self.description,
		    'resources': self.resources,
		    'status': self.status,
		    'created_at': self.created_at,
		    'updated_at': self.updated_at
	    }