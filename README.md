# Project Title

This is a Rest API for Logs. It exposes two Api's - GET and POST for posting and retreiving the logs for your application.

## Getting Started

Clone the repo - git clone https://github.com/gaurav-mishra1990/Rest-Api.git

### Prerequisites

Python 3.
pip3 - Python package manager.
Postgres - Create a empty database.
Elasticsearch - Create mappings as given by Postman collection.

### Installing

After cloning the repo -

1. Install virtualenv using pip - sudo python3 -m pip install virtualenv
2. Create a Virtual Environment - python3 -m venv ~/.virtualenvs/env_flask
3. Activate the Virtual Environment - source ~/.virtualenvs/env/bin/activate
4. Install the required Python packages - sudo python3 -m pip install -r requirements.txt
5. Set your environment variables in setup.sh
6. Source the setup file - source setup.sh
7. export PYTHONPATH=$PYTHONPATH:/<path..to..your..Rest..Api..directory>
8. In case of database - python3 manage.py db init
9. In case of database - python3 manage.py db migrate
10. In case of database - python3 manage.py db upgrade
11. Run the app - python3 app.py
