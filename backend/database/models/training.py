from datetime import datetime
from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class TrainingModel(db.Model):
    __tablename__ = 'training'

    training_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    weather = db.Column(JSON, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Training('{self.training_id}', '{self.datetime_display}')"


class TrainingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingModel
        include_fk = True
