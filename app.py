from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from database import get_tasks, add_task, delete_task, update_task

# Load .env file
load_dotenv()

# Configure Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure MongoDB
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
db = mongo.db  # Get database object

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data["_id"]), user_data["username"], user_data["password"])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if db.users.find_one({"username": username}):
            flash("Username already exists", "error")
            return redirect(url_for('signup'))
        
        new_user = {
            "username": username,
            "password": password  
        }
        db.users.insert_one(new_user)
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Username: {username}, Password: {password}")  # Debug info
        user_data = db.users.find_one({"username": username})
        print(f"User data: {user_data}")  # Debug info
        if user_data and user_data["password"] == password:
            user = User(str(user_data["_id"]), user_data["username"], user_data["password"])
            login_user(user, remember=False)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "error")
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def default():
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    tasks = get_tasks()  # Get all tasks from the database
    return render_template('index.html', tasks=tasks)

# Add task route
@app.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('add.html')
    title = request.form.get("title")
    description = request.form.get("description")
    status = "pending"
    task = {"title": title, "description": description, "status": status}
    add_task(task)
    return redirect(url_for('home'))

# Update task route
@app.route('/update/<task_id>', methods=['GET', 'POST'])
@login_required
def update(task_id):
    task = next((t for t in get_tasks() if t["_id"] == task_id), None)
    if not task:
        return "Task not found", 404 
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status")
        success = update_task(task_id, title, description, status)
        if success:
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Failed to update task {task_id}")
        return redirect(url_for('home'))
    return render_template('update.html', task=task)

# Delete task route (modified)
@app.route('/delete/<task_id>', methods=['GET','POST'])
@login_required
def delete(task_id):
    # Get the task first to check its status
    task = db.tasks.find_one({"_id": ObjectId(task_id)})
    
    if not task:
        flash("Task not found.", "error")
        return redirect(url_for('home'))
    task_status = task.get('status', '').lower()
    
    if request.method == 'POST': #If user confirm deletion
        success = delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully")
            flash("Task deleted successfully.", "success")
        else: 
            print(f"Failed to delete task {task_id}.")
            flash("Failed to delete task.", "error")
        
        # If the task was completed, stay on the completed page
        previous_page = request.referrer
        if previous_page and  "completed" in previous_page:
            return redirect(url_for('completed'))
        else:
            return redirect(url_for('home'))
    #If it is a get request
    return render_template('delete_confirm.html', task=task)

# Search tasks route
@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').lower()  # Get search keyword
    tasks = get_tasks()  
    filtered_tasks = []
    if query:
        # Filter tasks based on query
        filtered_tasks = [
            task for task in tasks
            if query in task.get('title', '').lower() or query in task.get('description', '').lower()
        ]
    return render_template('search.html', tasks=filtered_tasks)

# Completed tasks route - display completed tasks
@app.route('/completed')
@login_required
def completed():
    tasks = get_tasks()
    # Filter tasks with status "completed"
    completed_tasks = [task for task in tasks if task.get('status') == 'completed']
    return render_template('completed.html', tasks=completed_tasks)

# Mark task as incomplete route
@app.route('/incomplete/<task_id>', methods=['GET'])
@login_required
def mark_incomplete(task_id):
    # Update the task's status to "pending"
    success = update_task(task_id, status="pending")
    if success:
        flash("Task marked as incomplete.", "success")
    else:
        flash("Failed to mark task as incomplete.", "error")
    # Redirect to the completed tasks page after updating
    return redirect(url_for('completed'))

# Delete all completed tasks route
@app.route('/delete_all_completed', methods=['POST'])
@login_required
def delete_all_completed():
    # Delete all tasks with status "completed" from the tasks collection
    result = db.tasks.delete_many({"status": "completed"})
    if result.deleted_count > 0:
        flash(f"Deleted {result.deleted_count} completed tasks.", "success")
    else:
        flash("No completed tasks to delete.", "error")
    # Redirect back to the completed tasks page
    return redirect(url_for('completed'))

if __name__ == '__main__':
    app.run(debug=True)