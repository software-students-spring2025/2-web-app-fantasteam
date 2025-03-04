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


# Task Manager - Setup and Run Guide

This guide will help you **clone, set up, and run** the Task Manager Flask web application using **MongoDB Atlas** as the database.

---

## **🔹 Step 1: Clone the Repository**

1. Open your terminal (Command Prompt, PowerShell, or Git Bash).
2. Navigate to the location where you want to store the project.
3. Run the following command to **clone the repository** into a new folder named `TaskManager`:

   ```bash
   git clone https://github.com/software-students-spring2025/2-web-app-fantasteam.git TaskManager
   ```
4. Navigate into the project folder:

   ```bash
   cd TaskManager
   ```

---

## **🔹 Step 2: Set Up MongoDB Atlas**  

We will use **MongoDB Atlas** (Cloud Database) instead of a local MongoDB instance.

1. Sign up or log in to [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Create a new cluster:
   - Click **"Create a new cluster"**.
   - Select **"Shared Cluster"** (Free tier).
   - Follow the instructions and wait for your cluster to be created.
3. Go to **Database Deployment** → Click **"Connect"**.
4. Choose **"Connect your application"**.
5. Copy the connection string. It will look like this:
   
   ```
   mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/task_manager?retryWrites=true&w=majority
   ```

6. Inside the `TaskManager` project folder, create a new file named **`.env`** and add the following:

   ```env
   MONGO_URI="mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/task_manager?retryWrites=true&w=majority"
   MONGO_DBNAME="task_manager"
   SECRET_KEY="your_secret_key"
   FLASK_ENV="development"
   ```

   Replace `<username>`, `<password>`, and `<cluster-name>` with your actual MongoDB Atlas credentials.

---

## **🔹 Step 3: Install Dependencies**

Make sure you have **Python installed**, then run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

---

## **🔹 Step 4: Run the Flask App**

Once everything is set up, start the Flask application by running:

```bash
python app.py
```

If everything is configured correctly, you should see output like:

```
 * Running on http://127.0.0.1:5000/
```

---

## **🔹 Step 5: Open in Browser**

Now, open your browser and go to:

```
http://127.0.0.1:5000/
```

This will take you to the login page, where you can **sign up, log in, and start managing your tasks**.

🎉 Your **Task Manager App** is now running successfully!






























## Task boards
[Fantasteam - Sprint 1 Task Board](https://github.com/orgs/software-students-spring2025/projects/77)  
[Fantasteam - Sprint 2 Task Board](https://github.com/orgs/software-students-spring2025/projects/104)
