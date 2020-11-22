from datetime import datetime
from backend.database import db, ma
from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import column_property
import uuid


class SparepartModel(db.Model):
    __tablename__ = 'sparepart'

    sparepart_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    module = db.Column(db.String, nullable=False)
    stock = column_property(
        select([func.count(SparepartitemModel.sparepartitem_id)])
            .where(SparepartitemModel.sparepart_id == sparepart_id)
            .correlate_except(SparepartitemModel)
    )
    min_stock = db.Column(db.Integer, nullable=True)

    sparepart_item = db.relationship('SparepartitemModel', backref=db.backref('sparepart'))

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Sparepart[" \
               f"'{self.sparepart_id}': (" \
               f"'{self.module}', " \
               f"'{self.alarm}', " \
               f"'{self.datetime_display}'" \
               f")]"


class SparepartitemModel(db.Model):
    __tablename__ = 'sparepartitem'

    sparepartitem_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    sparepart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sparepart.sparepart_id'), nullable=False)

    condition = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

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


class SparepartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SparepartModel
        include_fk = True


class SparepartitemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SparepartitemModel
        include_fk = True
