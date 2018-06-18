# Flogger: A Simple Flask Blog

Part of the ["Professional Web Development Using Python Flask" course](https://flaskcourse.com).

Requires `python 3.6` installed.

## Local MySQL server
- Create the application user and password:
    - Logon to MySQL using root user
    - Create the Flogger database `CREATE DATABASE flogger;`
    - Create the floger user `CREATE USER 'flogger_user'@'%' IDENTIFIED BY 'flogger_password';`  
    - Give privileges to flogger user `GRANT ALL PRIVILEGES ON flogger.* TO 'flogger_user'@'%';` and `FLUSH PRIVILEGES;`
- Create a virtualenv: `python3 -m venv venv`
- Activate the virtualenv: `source venv/bin/activate`
- Install the packages: `pip install -r requirements.txt`
- Run `flask db init` to initialize migrations
- Run `flask db migrate` and `flask db upgrade` to create tables
- Run `flask runserver`
- Open `http://localhost:5000` on your browser
- To open a shell, just do `flask shell`
- Run tests by doing `python tests.py`
