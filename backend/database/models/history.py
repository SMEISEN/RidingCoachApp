from datetime import datetime
from backend.database import db, ma


class HistoryModel(db.Model):
    hist_id = db.Column(db.Integer, primary_key=True)
    #
    category = db.Column(db.String(20), nullable=False)  # Motor, Anbauteile, etc.
    name = db.Column(db.String(100), nullable=False)  # Öl gewechselt, etc.
    #
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    hours = db.Column(db.Float, nullable=False)  # 77.5 h
    #
    comment = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"History('{self.category}', '{self.name}', '{self.date}')"


class HistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel
        include_fk = True