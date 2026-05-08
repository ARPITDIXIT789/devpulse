from datetime import date, timedelta

from models.streak import Streak


def update_user_streak(user_id, db):
    streak = Streak.query.filter_by(user_id=user_id).first()
    if not streak:
        streak = Streak(user_id=user_id, current_streak=1, best_streak=1, last_active_date=date.today())
        db.session.add(streak)
        db.session.commit()
        return streak

    today = date.today()
    if streak.last_active_date == today:
        return streak

    if streak.last_active_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        streak.current_streak = 1

    streak.last_active_date = today
    streak.best_streak = max(streak.best_streak, streak.current_streak)
    streak.updated_at = today
    db.session.commit()
    return streak
