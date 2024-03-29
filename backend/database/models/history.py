from backend.database import db, ma
from backend.database.models.bike import BikeModel
from backend.database.models.maintenance import MaintenanceModel
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid


class HistoryModel(db.Model):
    __tablename__ = 'history'

    history_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    maintenance_id = db.Column(UUID(as_uuid=True), db.ForeignKey('maintenance.maintenance_id'), nullable=False)
    bike_id = db.Column(UUID(as_uuid=True), db.ForeignKey('bike.bike_id'), nullable=False)

    operating_hours = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    tags = db.Column(ARRAY(db.String), nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=db.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=db.utcnow, onupdate=db.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=db.utcnow)

    bike = db.relationship('BikeModel', backref=db.backref('history'))
    maintenance = db.relationship('MaintenanceModel',
                                  backref=db.backref('history', order_by='HistoryModel.operating_hours.desc()'))

    def __repr__(self):
        return f"History[" \
               f"'{self.history_id}': (" \
               f"'{self.operating_hours}', " \
               f"'{self.comment}', " \
               f"'{self.datetime_display}', " \
               f"mtn_id: '{self.maintenance_id}'," \
               f"bike_id: '{self.bike_id}'" \
               f")]"


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel
        include_fk = True
