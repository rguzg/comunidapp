Comunidapp
This project is made as a helper for the communities of teachers at university.
This project pretends to know before hand, the relationships that could lead to big and good investigations or projects that the teachers do.
Comunidapp is a web platforms that will know the actual state of the investigations and who made them, but also will display (with machine learning) the recomendations of the relationships of the teachers that, in another way, never would work together.

HOW TO START THE SERVER ON DEVELOPMENT MODE:
(Things that you need before: Git, Python3, MySQL Sever: i use XAAMP)
1. Clone the repo to your PC
- Optional: you can create a Python enviroment to install the things in the next step
2. Install the dependencies from 'requirements.txt' that is in the root folder
3. Create a DB called 'comunidapp' in MySQL (if need another DB, you should change the DB SETTINGS in file 'settings.py)
4. Call the command 'python3 manage.py makemigrations Users' at root folder (no errors should be thrown)
4. Call the command 'python3 manage.py makemigrations comunidad' at root folder (no errors should be thrown)
5. Call the command 'python3 manage.py migrate' at root folder (no errors should be thrown)
6. Call the command 'python3 manage.py createsuperuser' and give the information asked (no errors should be thrown) 
7. Call this command in the project root folder: 'python3 manage.py runserver'
8. Done!
9. You should be able to go to localhost:8000 and see the project running. You need to log-in with the user you created in the step #6 to see the full platform.

