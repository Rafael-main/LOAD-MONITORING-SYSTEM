# Load Monitoring Application

### Tech Stack
- HTML
- CSS
- Jquery
- Bootstrap 5.3
- Flask (python)
- SQLite

### Requirements
1. Intall Python https://www.python.org/downloads/
2. Install SQLite3 https://www.sqlite.org/download.html

### After installation do the following
1. ``` cd loadmonitoring ```
2. Create python virtual env with the following command in the command l ```python -m venv venv ```
3. activate virtual env by using the command ``` \venv\Scripts\activate ```
4. install all the required modules using the command ``` pip install -r requirements.txt ```

### Setup database
1. Set everything provided above befor taking this step.
2. After activating virtual env input the following command in the command line ``` export FLASK_APP=app ```
3. Then use flask's interactive shell using ``` flask shell ```
4. To create the database input the following command in the flask's interactive shell: 
 - first import db```>>> from app import db ```
 - next is to import the models provided in the models.py through the following command ```>>> from app.models import User, Department, Room, Load ```
 - Delete if the database already exists by using the command ```>>> db.drop_all() ```
 - Finally create the database with the following command ```>>> db.create_all() ```
5. Exit the flask shell with the ```>>> exit() ``` command

### Running the web app
1. Run the following command: ```python run.py ```