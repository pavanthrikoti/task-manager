from flask import Flask, render_template, request, jsonify
import json
import os
from uuid import uuid4  # For unique IDs

app = Flask(__name__)

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
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
    app.run(debug=True)