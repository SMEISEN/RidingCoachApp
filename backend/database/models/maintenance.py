from datetime import datetime
from backend.database import db, ma


class MaintenanceModel(db.Model):
    mtn_id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String(20), nullable=False)  # Motor, Anbauteile, etc.
    name = db.Column(db.String(100), unique=True, nullable=False)  # Öl gewechselt, etc.
    hours_interval = db.Column(db.Float, nullable=False)  # 5h, 10h, ...
    hours_last = db.Column(db.Float)  # 77.5 h

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Maintainance('{self.category}', '{self.name}', '{self.mtn_id}')"


class MaintenanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MaintenanceModel
        include_fk = True
