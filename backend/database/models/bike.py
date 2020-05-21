from backend.database import db, ma


class BikeModel(db.Model):
    operating_hours = db.Column(db.Float, primary_key=True)
    #
    manufacturer = db.Column(db.String(15), nullable=True)
    model = db.Column(db.String(15), nullable=True)
    ccm = db.Column(db.Float, nullable=True)
    stroke = db.Column(db.Float, nullable=True)
    piston = db.Column(db.Float, nullable=True)
    year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Bike('{self.operating_hours}', '{self.date_posted}')"


class BikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BikeModel
        include_fk = True