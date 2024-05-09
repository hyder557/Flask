from app import db

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer)
    unit = db.Column(db.String(20))
    unit_price = db.Column(db.Float)
    total_value = db.Column(db.Float)
    expiration_date = db.Column(db.Integer)
    supplier = db.Column(db.String(255))
    update_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price is not None else None,
            'total_value': float(self.total_value) if self.total_value is not None else None,
            'expiration_date': self.expiration_date,
            'supplier': self.supplier,
            'update_time': self.update_time.strftime('%Y-%m-%d') if self.update_time is not None else None,
            'description': self.description
        }
