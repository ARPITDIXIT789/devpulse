from datetime import date

from . import db


class Streak(db.Model):
    __tablename__ = "streaks"

    id = db.Column(db.Integer, primary_key=True)
    current_streak = db.Column(db.Integer, default=0, nullable=False)
    best_streak = db.Column(db.Integer, default=0, nullable=False)
    last_active_date = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.Date, default=date.today)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    def to_dict(self):
        return {
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
            "last_active_date": self.last_active_date.isoformat() if self.last_active_date else None,
        }
