from datetime import timedelta, date

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import func

from models.task import Task
from models.streak import Streak
from utils.github_commits import get_today_commit_count


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.get("/stats")
@jwt_required()
def get_stats():
    user_id = int(get_jwt_identity())

    total_tasks = Task.query.filter_by(user_id=user_id).count()
    done_tasks = Task.query.filter_by(user_id=user_id, status="done").count()
    in_progress_tasks = Task.query.filter_by(user_id=user_id, status="in_progress").count()

    weekly_start = date.today() - timedelta(days=6)
    weekly_rows = (
        Task.query.with_entities(func.date(Task.created_at), func.count(Task.id))
        .filter(Task.user_id == user_id, Task.created_at >= weekly_start)
        .group_by(func.date(Task.created_at))
        .all()
    )
    weekly_map = {row[0].isoformat(): row[1] for row in weekly_rows}

    weekly_progress = []
    for i in range(7):
        d = weekly_start + timedelta(days=i)
        weekly_progress.append({"date": d.isoformat(), "tasks": weekly_map.get(d.isoformat(), 0)})

    streak = Streak.query.filter_by(user_id=user_id).first()
    commits_today = get_today_commit_count()

    productivity_score = int((done_tasks / total_tasks) * 100) if total_tasks else 0

    return jsonify(
        {
            "today_stats": {
                "tasks": total_tasks,
                "commits": commits_today,
                "coding_hours": 0,
                "score": productivity_score,
                "in_progress": in_progress_tasks,
            },
            "weekly_progress": weekly_progress,
            "streak": streak.to_dict() if streak else {"current_streak": 0, "best_streak": 0},
        }
    )
