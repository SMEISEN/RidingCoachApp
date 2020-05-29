from datetime import datetime
from backend.database import db, ma
from backend.database.models.bike import BikeModel
from sqlalchemy.dialects.postgresql import UUID
import uuid


class HistoryModel(db.Model):
    __tablename__ = 'history'

    history_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    maintenance_id = db.Column(UUID(as_uuid=True), db.ForeignKey('maintenance.maintenance_id'), nullable=False)
    bike_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bike.bike_id'), nullable=False)

    operating_hours = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    bike = db.relationship('BikeModel', backref=db.backref('history'))

    def __repr__(self):
        return f"History('{self.category}', '{self.name}', '{self.date}')"


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel
        include_fk = True
