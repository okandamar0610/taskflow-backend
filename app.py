import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from models import db, Task
from flags import flags, init_flags

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow"
)
db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()

init_flags()


@app.route("/api/health")
def health():
    return jsonify(status="ok")


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.order_by(Task.id).all()
    return jsonify([t.to_dict() for t in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    if "done" in data:
        task.done = bool(data["done"])
    if "title" in data and data["title"].strip():
        task.title = data["title"].strip()
    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return "", 204


@app.route("/api/meta")
def meta():
    """Values controlled live by CloudBees Unify feature flags."""
    return jsonify(
        show_due_date_banner=flags.show_due_date_banner.is_enabled(),
        task_priority_label=flags.task_priority_label.get_value(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
