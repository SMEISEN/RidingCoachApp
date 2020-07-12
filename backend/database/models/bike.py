from datetime import datetime
from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class BikeModel(db.Model):
    __tablename__ = 'bike'

    bike_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    operating_hours = db.Column(db.Float, nullable=False)

    manufacturer = db.Column(db.String(15), nullable=False)
    model = db.Column(db.String(15), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    ccm = db.Column(db.Float, nullable=True)
    stroke = db.Column(db.Float, nullable=True)
    piston = db.Column(db.Float, nullable=True)
    slick_front = db.Column(db.String(50), nullable=True)
    slick_rear = db.Column(db.String(50), nullable=True)
    rain_front = db.Column(db.String(50), nullable=True)
    rain_rear = db.Column(db.String(50), nullable=True)
    setup = db.Column(JSON, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return f"Bike[" \
               f"'{self.bike_id}': (" \
               f"'{self.manufacturer}', " \
               f"'{self.model}', " \
               f"'{self.year}', " \
               f"'{self.operating_hours}'h" \
               f")]"


class BikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BikeModel
        include_fk = True
