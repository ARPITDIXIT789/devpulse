from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import db
from models.task import Task
from utils.helpers import update_user_streak


tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@tasks_bp.get("")
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.post("")
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    if not title:
        return jsonify({"message": "Task title is required"}), 400

    due_date = None
    if data.get("due_date"):
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

    task = Task(
        title=title,
        description=data.get("description"),
        status=data.get("status", "pending"),
        progress=int(data.get("progress", 0)),
        due_date=due_date,
        user_id=user_id,
    )
    db.session.add(task)
    db.session.commit()

    update_user_streak(user_id, db)
    return jsonify(task.to_dict()), 201


@tasks_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    data = request.get_json() or {}
    if "title" in data:
        task.title = data["title"].strip() or task.title
    if "description" in data:
        task.description = data["description"]
    if "status" in data:
        task.status = data["status"]
    if "progress" in data:
        task.progress = int(data["progress"])
    if "due_date" in data:
        task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data["due_date"] else None

    db.session.commit()
    update_user_streak(user_id, db)
    return jsonify(task.to_dict())


@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
