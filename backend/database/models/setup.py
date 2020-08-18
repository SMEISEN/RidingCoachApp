from datetime import datetime
from backend.database import db, ma
from backend.database.models.bike import BikeModel
from backend.database.models.training import TrainingModel
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class SetupModel(db.Model):
    __tablename__ = 'setup'

    setup_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    training_id = db.Column(UUID(as_uuid=True), db.ForeignKey('training.training_id'), nullable=False)
    bike_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bike.bike_id'), nullable=False)

    operating_hours = db.Column(db.Float, nullable=False)
    weather_current = db.Column(JSON, nullable=True)
    slick_pressure_front = db.Column(db.Float, nullable=True)
    slick_pressure_rear = db.Column(db.Float, nullable=True)
    rain_pressure_front = db.Column(db.Float, nullable=True)
    rain_pressure_rear = db.Column(db.Float, nullable=True)
    setup = db.Column(JSON, nullable=True)
    comment = db.Column(db.Text, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    bike = db.relationship(
        'BikeModel', backref=db.backref('setups', order_by='SetupModel.datetime_display.asc()'))
    training = db.relationship(
        'TrainingModel', backref=db.backref('setups', order_by='SetupModel.datetime_display.asc()'))

    def __repr__(self):
        return f"Setup[" \
               f"'{self.setup_id}': (" \
               f"'{self.operating_hours}', " \
               f"'{self.comment}', " \
               f"'{self.datetime_display}', " \
               f"training_id: '{self.training_id}', " \
               f"bike_id: '{self.bike_id}'" \
               f")]"


class SetupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SetupModel
        include_fk = True
