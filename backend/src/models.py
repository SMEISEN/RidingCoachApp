from datetime import datetime
from backend.src import db, ma


class Maintenance(db.Model):
    # fixed
    mtn_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), nullable=False)  # Motor, Anbauteile, etc.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Öl gewechselt, etc.
    hours_interval = db.Column(db.Float, nullable=False)  # 5h, 10h, ...
    # variable
    date_last = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hours_last = db.Column(db.Float, nullable=False)  # 77.5 h
    hours_left = db.Column(db.Float, nullable=False)  # hours_now - hours_last
    status = db.Column(db.Float, nullable=False)  # hours_left/hours_interval * 100 %

    def __repr__(self):
        return f"Maintainance('{self.category}', '{self.name}', '{self.mtn_id}')"


class MaintenanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Maintenance
        include_fk = True


class Bike(db.Model):
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


class History(db.Model):
    hist_id = db.Column(db.Integer, primary_key=True)
    #
    category = db.Column(db.String(20), nullable=False)  # Motor, Anbauteile, etc.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Öl gewechselt, etc.
    #
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hours = db.Column(db.Float, nullable=False)  # 77.5 h
    #
    comment = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"History('{self.category}', '{self.name}', '{self.date}')"