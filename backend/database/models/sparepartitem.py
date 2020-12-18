from datetime import datetime
from backend.database import db, ma
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid


class SparepartitemModel(db.Model):
    __tablename__ = 'sparepartitem'

    sparepartitem_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sparepart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sparepart.sparepart_id'), nullable=False)

    condition = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Sparepartitem[" \
               f"'{self.sparepartitem_id}': (" \
               f"'{self.condition}', " \
               f"'{self.description}', " \
               f"'{self.datetime_display}'" \
               f")]"


class SparepartitemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SparepartitemModel
        include_fk = True
