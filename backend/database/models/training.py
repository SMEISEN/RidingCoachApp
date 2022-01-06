from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class TrainingModel(db.Model):
    __tablename__ = 'training'

    training_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    location = db.Column(db.String, nullable=False)
    weather_hourly = db.Column(JSON, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, server_default=db.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, server_default=db.utcnow, onupdate=db.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, server_default=db.utcnow)

    def __repr__(self):
        return f"Training[" \
               f"'{self.training_id}': (" \
               f"'{self.location}', " \
               f"'{self.datetime_display}'" \
               f")]"


class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingModel
        include_fk = True
