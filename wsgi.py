import sys
import os

# Get your PythonAnywhere username from the path
username = os.path.expanduser('~').split('/')[-1]
path = f'/home/{username}/mywebsite'

# Add your project directory to the sys.path
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import your app
from app import app as application 