from datetime import datetime
from backend.database import db, ma
from backend.database.models.session import SessionModel
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class LaptimeModel(db.Model):
    __tablename__ = 'laptime'

    lap_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    session_id = db.Column(UUID(as_uuid=True), db.ForeignKey('session.session_id'), nullable=False)

    lap_no = db.Column(db.Integer, nullable=False)
    valid = db.Column(db.Boolean, nullable=False, default=True)
    track_layout = db.Column(db.String, nullable=False, default="A")
    laptime_seconds = db.Column(db.Float, nullable=False)
    sectors = db.Column(JSON, nullable=False)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    session = db.relationship(
        'SessionModel',
        backref=db.backref('laptimes', order_by='LaptimeModel.datetime_display.asc()'))

    def __repr__(self):
        return f"Lap time[" \
               f"'{self.lap_id}': (" \
               f"'{self.datetime_display}', " \
               f"training_id: '{self.training_id}', " \
               f"bike_id: '{self.bike_id}', " \
               f"setup_id: '{self.setup_id}', " \
               f")]"


class LaptimeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LaptimeModel
        include_fk = True
