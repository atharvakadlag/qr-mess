from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Main(db.Model):
    """model for the data table
    stores time and username
    """
    __tablename__ = 'main'

    date = db.Column(db.DateTime, primary_key=True, default=datetime.now().date())
    name = db.Column(db.String(256), index=True)
    slot = db.Column(db.String(32), index=True)

    __table_args__ = (
        db.UniqueConstraint('date', 'name', 'slot', name='_entry_uc'),
    )