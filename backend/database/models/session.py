from backend.database import db, ma
from backend.database.models.setup import SetupModel
from backend.database.models.training import TrainingModel
from backend.database.models.bike import BikeModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class SessionModel(db.Model):
    __tablename__ = 'session'

    session_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    training_id = db.Column(UUID(as_uuid=True), db.ForeignKey('training.training_id'), nullable=False)
    setup_id = db.Column(UUID(as_uuid=True), db.ForeignKey('setup.setup_id'), nullable=True)
    bike_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bike.bike_id'), nullable=True)

    application = db.Column(db.String(50), nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=db.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=db.utcnow, onupdate=db.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=db.utcnow)

    bike = db.relationship(
        'BikeModel', backref=db.backref('sessions', order_by='SessionModel.datetime_display.asc()'))
    training = db.relationship(
        'TrainingModel', backref=db.backref('sessions', order_by='SessionModel.datetime_display.asc()'))
    setup = db.relationship(
        'SetupModel', backref=db.backref('sessions', order_by='SessionModel.datetime_display.asc()'))

    def __repr__(self):
        return f"Session[" \
               f"'{self.session_id}': (" \
               f"'{self.datetime_display}', " \
               f"training_id: '{self.training_id}', " \
               f"bike_id: '{self.bike_id}', " \
               f"setup_id: '{self.setup_id}', " \
               f")]"


class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SessionModel
        include_fk = True
