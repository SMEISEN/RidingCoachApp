from backend.database import db, ma
from backend.database.models.sparepartitem import SparepartitemModel
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class SparepartModel(db.Model):
    __tablename__ = 'sparepart'

    sparepart_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = db.Column(db.String, nullable=False)
    items = db.relationship('SparepartitemModel', backref=db.backref('sparepart'))

    module = db.Column(db.String, nullable=False)
    min_stock = db.Column(db.Integer, nullable=True)
    current_stock = db.column_property(
        db.select([func.sum(SparepartitemModel.stock)])
            .where(SparepartitemModel.sparepart_id == sparepart_id)
            .correlate_except(SparepartitemModel)
    )

    datetime_created = db.Column(db.DateTime, nullable=False, server_default=db.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, server_default=db.utcnow, onupdate=db.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, server_default=db.utcnow)

    def __repr__(self):
        return f"Sparepart[" \
               f"'{self.sparepart_id}': (" \
               f"'{self.module}', " \
               f"'{self.alarm}', " \
               f"'{self.datetime_display}'" \
               f")]"


class SparepartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SparepartModel
        include_fk = True
