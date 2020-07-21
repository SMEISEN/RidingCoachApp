from datetime import datetime
from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class MaintenanceModel(db.Model):
    __tablename__ = 'maintenance'

    maintenance_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    category = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    interval_type = db.Column(db.String(25), nullable=False)
    interval_amount = db.Column(db.Float, nullable=True)
    interval_unit = db.Column(db.String(25), nullable=True)
    tags_default = db.Column(JSON, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Maintenance[" \
               f"'{self.maintenance_id}': (" \
               f"'{self.category}', " \
               f"'{self.name}', " \
               f"'{self.interval_amount}', " \
               f"'{self.interval_unit}', " \
               f"'{self.interval_type}'" \
               f")]"


class MaintenanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MaintenanceModel
        include_fk = True
