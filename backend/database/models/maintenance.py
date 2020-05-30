from datetime import datetime
from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID
import uuid


class MaintenanceModel(db.Model):
    __tablename__ = 'maintenance'

    maintenance_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    category = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    interval_amount = db.Column(db.Float, nullable=False)
    interval_unit = db.Column(db.String(25), nullable=False)
    interval_type = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"Maintenance('{self.maintenance_id}', '{self.category}', '{self.name}')"


class MaintenanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MaintenanceModel
        include_fk = True
