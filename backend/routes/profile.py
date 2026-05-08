from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.task import Task
from models.user import User
from models.streak import Streak


profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.get("")
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    streak = Streak.query.filter_by(user_id=user_id).first()

    total_tasks = Task.query.filter_by(user_id=user_id).count()
    completed_tasks = Task.query.filter_by(user_id=user_id, status="done").count()

    return jsonify(
        {
            "user": user.to_dict(),
            "stats": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": int((completed_tasks / total_tasks) * 100) if total_tasks else 0,
                "current_streak": streak.current_streak if streak else 0,
                "best_streak": streak.best_streak if streak else 0,
            },
        }
    )
