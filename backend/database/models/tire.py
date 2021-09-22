from datetime import datetime
from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class TireModel(db.Model):
    __tablename__ = 'tire'

    tire_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    bike_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bike.bike_id'), nullable=False)

    rim = db.Column(db.String(15), nullable=True)

    category = db.Column(db.String(5), nullable=False)
    manufacturer = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(25), nullable=True)
    compound = db.Column(db.String(10), nullable=True)
    axis = db.Column(db.String(5), nullable=False)
    dimension = db.Column(db.String(15), nullable=True)
    dot = db.Column(db.String(4), nullable=False)

    condition = db.Column(JSON, nullable=False, default={
        "left_outer": 1.0,
        "left_middle": 1.0,
        "center": 1.0,
        "right_middle": 1.0,
        "right_outer": 1.0
    })
    operating_hours = db.Column(db.Float, nullable=False)

    comment = db.Column(db.Text, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Maintenance[" \
               f"'{self.maintenance_id}': (" \
               f"'{self.category}', " \
               f"'{self.name}', " \
               f"'{self.interval_amount}', " \
               f"'{self.interval_unit}', " \
               f"'{self.interval_type}'" \
               f")]"


class TireSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TireModel
        include_fk = True
