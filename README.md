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
4. Write the command 'cd C:\[the directory of the project folder]'
5. Build the project to Docker with the command 'docker compose build'
6. After the setup, check Docker Desktop images and container if the project is now available.
7. Run the container to test.
