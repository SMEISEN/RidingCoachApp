from datetime import datetime
from backend.database import db, ma


class MaintenanceModel(db.Model):
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
        model = MaintenanceModel
        include_fk = True