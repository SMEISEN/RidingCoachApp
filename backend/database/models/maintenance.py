from datetime import datetime
from backend.database import db, ma
from backend.database.models.history import HistoryModel


class MaintenanceModel(db.Model):
    __tablename__ = 'maintenance'

    maintenance_id = db.Column(db.Integer, primary_key=True)

    category = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    interval_amount = db.Column(db.Float, nullable=False)
    interval_unit = db.Column(db.String(25), nullable=False)
    interval_type = db.Column(db.String(25), nullable=False)

    history = db.relationship('HistoryModel', backref=db.backref('maintenance'))

    def __repr__(self):
        return f"Maintenance('{self.maintenance_id}', '{self.category}', '{self.name}')"


class MaintenanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MaintenanceModel
        include_fk = True
