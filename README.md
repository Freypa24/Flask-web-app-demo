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

# Installation of the web app:
1. Ensure you have Pycharm community or other IDE, and Docker Desktop. Download it if not
2. Download the project repository from here. Then, open and copy the project's folder directory
3. Open Windows CMD
4. Write the command 'cd C:\[the directory of the project folder]\Midterm_app'
5. Build the project to Docker with the command 'docker compose build'
6. After the setup, check Docker Desktop images and container if the project is now available.
7. Run the container to test.

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
