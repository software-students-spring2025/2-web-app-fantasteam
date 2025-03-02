from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from database import get_tasks, add_task, delete_task, update_task

# 加载 .env 文件
load_dotenv()

# 配置 Flask 应用
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# 配置 MongoDB
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
db = mongo.db  # 获取数据库对象

# Flask-Login 配置
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户模型
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
        print(f"Username: {username}, Password: {password}")  # 调试信息
        user_data = db.users.find_one({"username": username})
        print(f"User data: {user_data}")  # 调试信息
        if user_data and user_data["password"] == password:
            user = User(str(user_data["_id"]), user_data["username"], user_data["password"])
            login_user(user,remember=False)
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password","error")
    return render_template('login.html')

# 注销路由
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 主页路由 - 显示所有任务
@app.route('/')
@login_required
def home():
    tasks = get_tasks()  # 从数据库获取所有任务
    return render_template('index.html', tasks=tasks)

# 添加任务路由
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

# 更新任务路由
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

# 删除任务路由
@app.route('/delete/<task_id>', methods=['POST'])
@login_required
def delete(task_id):
    success = delete_task(task_id)
    if success:
        print(f"Task {task_id} deleted successfully")
    else: 
        print(f"Failed to delete task {task_id}.")
    tasks = get_tasks()  # 从数据库获取所有任务
    return render_template('index.html', tasks=tasks)

# 搜索任务路由
@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').lower()  # 获取搜索关键字
    tasks = get_tasks()  
    filtered_tasks = []
    if query:
        # 根据关键字过滤任务
        filtered_tasks = [
            task for task in tasks
            if query in task.get('title', '').lower() or query in task.get('description', '').lower()
        ]
    return render_template('search.html', tasks=filtered_tasks)

# 已完成任务路由 - 显示已完成的任务
@app.route('/completed')
@login_required
def completed():
    tasks = get_tasks()
    # 过滤状态为 "completed" 的任务
    completed_tasks = [task for task in tasks if task.get('status') == 'completed']
    return render_template('completed.html', tasks=completed_tasks)

if __name__ == '__main__':
    app.run(debug=True)