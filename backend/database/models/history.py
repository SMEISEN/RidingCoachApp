from datetime import datetime
from backend.database import db, ma


class HistoryModel(db.Model):
    __tablename__ = 'history'

    history_id = db.Column(db.Integer, primary_key=True)

    maintenance_id = db.Column(db.String, db.ForeignKey('maintenance.maintenance_id'), nullable=False)

    operating_hours = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    datetime_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    datetime_display = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"History('{self.category}', '{self.name}', '{self.date}')"


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel
        include_fk = True
