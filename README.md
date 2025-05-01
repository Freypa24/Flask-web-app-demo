# Flask-web-app-demo

The Tech Stack is : Python (Flask) + Postgres + Docker + (Maybe) Nginx

# Note to Developers:
In the repository, there is a file named '.gitignore' that holds the name of files to be excluded from github commit.
It includes a .env file, which is NECESSARY to run the web app. As part of security, it is ALWAYS excluded from any github repositories.
You will be introduced to creating the .env file to proceed with the installation of the web app.

# Installation of Docker:
1. Go to your bios, enable Hardware Virtualization
2. Go to Docker website and download Docker Desktop for Windows - x84_64
3. Open the installer and use WSL-2
4. Run Docker Desktop

# Installation of the web app (Other ide):
1. Ensure you have Pycharm community or other IDE, and Docker Desktop. Download it if not
2. Download the project repository from here. Then, open and copy the project's folder directory from your IDE
3. If its a new project, open terminal and type [python -m venv venv] without the [].
4. Activate the venv by typing venv/Scripts/activate
5. Create a .env inside the project folder and paste the variables from the given message.
6. Open windows terminal
7. Write the command 'cd C:\[the directory of the project folder]\Midterm_app'
8. Build the project to Docker with the command 'docker compose build'
9. After the setup, check Docker Desktop images, run if the project is now available.
10. After running, turn it off and then go back to terminal and type the command 'docker compose up -d --build'
11. Once the project is running in docker, initialize the database and the seed admin.
12. To initialize database, connect to the flask app in terminal with the command 'Docker exec -it [container name]-[service-name-app]-1 /bin/sh'
13. Next, run the commands in order; rm -rf migrations, flask db init, flask db migrate, flask db upgrade.
14. Lastly, run this command to initialize the admin 'Docker exec -it midterm_web-web-app-1 python app/run/seed_admin.py'
15. Test the website.

# Commands:
CMD Terminal database:
- Docker exec -it [container name]-[service-name-db]-1 -U [database user] -d [database name] - This will connect you to the database as the user in Docker. You can use this to run database commands
- \dt - Shows all tables
- \q - Exit the connection

CMD Terminal flask-migrate commands:
- Docker exec -it [container name]-[service-name-app]-1 /bin/sh - This is a connection to the web app to perform flask db migrations.
- rm -rf migrations - Removes the migrations folder incase of failure. This is to restart but you will lose all data
- flask db init - To initiate the migrations folder
- flask db migrate -m "Write your message inside these quotation marks" - When you want to update your database, you must first migrate it. This will make your changes be manually reviewed before you put it into the database.
- flask db upgrade - When you do this, you are now telling alembic (The application) to finalize and update the database.
- flask db downgrade - This is when you made a mistake and want to revision your LAST upgrade. It will remove all changes of the last upgrade.

CMD Terminal Docker:
- Docker Compose Build - Initial build of the web app.
- Docker Compose up --build - Updates the built web app inside Docker
- Docker compose up -d --build - Keeps the terminal interactable after update and running.
- Docker exec -it midterm_web-web-app-1 python app/run/seed_admin.py - This initializes the admin user and workforce.
