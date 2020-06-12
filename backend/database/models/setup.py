from datetime import datetime
from backend.database import db, ma
from backend.database.models.bike import BikeModel
from backend.database.models.training import TrainingModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class SetupModel(db.model):
    __tablename__ = 'setup'

    setup_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    training_id = db.Column(UUID(as_uuid=True), db.ForeignKey('training.training_id'), nullable=False)
    bike_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bike.bike_id'), nullable=False)

    operating_hours = db.Column(db.Float, nullable=False)
    weather = db.Column(JSON, nullable=True)
    slick_pressure_front = db.Column(db.Float, nullable=True)
    slick_pressure_rear = db.Column(db.Float, nullable=True)
    rain_pressure_front = db.Column(db.Float, nullable=True)
    rain_pressure_rear = db.Column(db.Float, nullable=True)
    setup = db.Column(JSON, nullable=True)
    comment = db.Column(db.Text, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    bike = db.relationship('BikeModel', backref=db.backref('setup'))
    training = db.relationship('TrainingModel',
                               backref=db.backref('setup', order_by='SetupModel.datetime_display.asc()'))

    def __repr__(self):
        return f"Setup('{self.setup_id}', '{self.operating_hours}', '{self.datetime_display}')"


class SetupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SetupModel
        include_fk = True