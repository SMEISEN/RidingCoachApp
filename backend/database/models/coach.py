from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON, ARRAY
import uuid


class CoachModel(db.Model):
    __tablename__ = 'coach'

    coach_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    category = db.Column(db.String(6), nullable=False)
    symptom = db.Column(db.JSON, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    questions = db.Column(ARRAY(db.String), nullable=True, default=[])
    advice = db.Column(JSON, nullable=False)

    datetime_created = db.Column(db.DateTime, nullable=False, server_default=db.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, server_default=db.utcnow, onupdate=db.utcnow)

    def __repr__(self):
        return f"Coach[" \
               f"'{self.coach_id}': (" \
               f"'{self.category}', " \
               f"'{self.symptom}'" \
               f")]"


class CoachSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CoachModel
        include_fk = True
