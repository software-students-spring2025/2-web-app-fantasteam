# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.

## Team members

- Chuqiao Huang (ch3807) - [GitHub Profile](https://github.com/ChuqiaoHuang)
- Jasmine Zhang (jz5144) - [GitHub Profile](https://github.com/Jasminezhang666666)
- Shipeng Zhao (sz3822) - [GitHub Profile](https://github.com/Tonyzsp)
- Leo Wu (jw7026) - [GitHub Profile](https://github.com/leowu777)



## Product vision statement

Our web-based task manager empowers users to seamlessly add, search, edit, and complete tasks with an intuitive interface that transforms everyday productivity.

## User stories

1. As a user, I want to see a list of all my tasks so that I can manage my to-do items effectively.
2.  As a user, I want to add a new task so that I can track new to-do items.
3. As a user, I want to edit a task so that I can update its details if needed.
4. As a user, I want to delete a task so that I can remove completed or unnecessary tasks.
5. As a user, I want to search for tasks so that I can quickly find specific items.
6. As a user, I want to see only my completed tasks so that I can review what I have accomplished.
7. As a user, I want to mark a task as completed so that I can keep track of finished work.
8. As a user, I want to log in so that only I can manage my tasks.
9. As a user, I want to log out so that my tasks remain secure.
10.  As a user, I want my task list to be private so that no one else can see or edit it.
11. As a developer, I want to store my database credentials securely so that my data is not exposed in version control.
12. As a developer, I want to deploy the app so that users can access it from anywhere.  
[View these User Stories in an 'Issues' Section](https://github.com/software-students-spring2025/2-web-app-fantasteam/issues)

## Steps necessary to run the software

See instructions. Delete this line and place instructions to download, configure, and run the software here.

## Task boards
[Fantasteam - Sprint 1 Task Board](https://github.com/orgs/software-students-spring2025/projects/77)  
[Fantasteam - Sprint 2 Task Board](https://github.com/orgs/software-students-spring2025/projects/104)

# Flask-MongoDB Web App Example

![Dockerize badge](https://github.com/nyu-software-engineering/flask-pymongo-web-app-example/actions/workflows/build.yaml/badge.svg)

An example of a full-stack web application, built in Python with `Flask` and `PyMongo`.

## Quick Test Drive

The fastest way to see the example app in action on your own computer is to use [Docker](https://www.docker.com).

First, you must:

- Install and run [Docker Desktop](https://www.docker.com/get-started)
- Create a [DockerHub](https://hub.docker.com/signup) account

## Option 1: Using Docker Compose

Use Docker Compose to boot up both the `MongoDB` database and the `Flask` web app with one command:

```bash
docker compose up --force-recreate --build
To run in detached/background mode, add -d. To stop the containers when done, use:

docker compose down
If you see an error that a port is already in use, edit the first port number for the flask-app or mongodb service in the docker-compose.yml file and retry. For example, change:

flask-app:
  ports:
    - "10000:5000"
Then, update FLASK_PORT in docker-compose.yml accordingly.

View the app in your browser:

Open a web browser and go to http://localhost:5000 (or the custom port you assigned).
Note: If you edit any project files, you must restart the containers.

Option 2: Running Services Separately
Start a MongoDB database first:

docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest
Then start the flask-app:

docker run -ti --rm -d -p 5000:5000 -e MONGO_DBNAME=flask-mongodb-web-app-example -e MONGO_URI="mongodb://admin:secret@host.docker.internal:27017" bloombar/flask-mongodb-web-app-example
If you see a port conflict, change 5000 to another number, e.g., 10000:5000.

Access the app:

Open http://localhost:5000 (or the port you set).
Setup for Editing
1. Build and Launch MongoDB
Start a MongoDB database:

docker run --name mongodb_dockerhub -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest
To interact with the database:

docker exec -ti mongodb_dockerhub mongosh -u admin -p secret
Show available databases:

show dbs
Use the database:

use example
List documents in the messages collection:

db.messages.find()
Exit:

exit
2. Create a .env File
Create a .env file and add:

MONGO_DBNAME=taskmanager
MONGO_URI="mongodb://admin:secret@localhost:27017/taskmanager?authSource=admin&retryWrites=true&w=majority"
SECRET_KEY="fantasteam2025"
FLASK_ENV="development"
FLASK_PORT="5000"
3. Set Up a Python Virtual Environment
Using pipenv
Install pipenv:

pip3 install pipenv
Activate:

pipenv shell
Dependencies will be installed automatically.

Using venv
Create a virtual environment:

python3 -m venv .venv
Activate:

# On Mac/Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate.bat
Install dependencies:

pip3 install -r requirements.txt
4. Run the App
Development Mode
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
Or:

python3 -m flask run --host=0.0.0.0 --port=5000
Production Mode
export FLASK_APP=app.py
export FLASK_ENV=production
gunicorn --config gunicorn_config.py wsgi:app
Then visit http://0.0.0.0:8080 in your browser.

Features
User authentication (signup, login, logout)
Task management (add, update, delete, mark as completed)
Search tasks by title or description
View completed tasks
Secure with Flask-Login
