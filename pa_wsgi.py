import os, sys
from dotenv import load_dotenv

python_anywhere_username = 'jorge3'
path = '/home/' + python_anywhere_username + '/opt/flogger'
if path not in sys.path:
    sys.path.append(path)

load_dotenv(os.path.join(path, '.flaskenv'))

from application import create_app
app = create_app()

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(app, evalex=True)
