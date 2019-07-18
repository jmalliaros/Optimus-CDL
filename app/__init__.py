import os
from flask import Flask
from config import Config

app = Flask(__name__)
app.port = int(os.environ.get('PORT', 6000))

from app import routes
from app import optimusform
