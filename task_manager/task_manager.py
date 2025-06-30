from flask import Flask, render_template, request, jsonify
import json
import os
from uuid import uuid4  # For unique IDs
from waitress import serve  # Add waitress for production

app = Flask(__name__)

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
            # Assign IDs to tasks that don't have them
            for task in tasks:
                if 'id' not in task:
                    task['id'] = str(uuid4())
            return tasks
    return []

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

@app.route('/', methods=['GET'])
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    task_description = request.form.get('task')
    if task_description and task_description.strip():
        new_task = {
            'id': str(uuid4()),  # Generate unique ID
            'description': task_description,
            'completed': False
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return jsonify(tasks)

@app.route('/toggle/<string:task_id>', methods=['PUT'])
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task.get('id') == task_id:
            task['completed'] = not task['completed']
            save_tasks(tasks)
            return jsonify(tasks)
    return jsonify(tasks), 404  # Task not found

@app.route('/delete/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task.get('id') != task_id]
    save_tasks(tasks)
    return jsonify(tasks)

if __name__ == '__main__':
    # Get port from environment, default to 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 for Render
    serve(app, host='0.0.0.0', port=port)
