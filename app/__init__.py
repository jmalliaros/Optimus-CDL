import os
from flask import Flask
from config import Config

app = Flask(__name__)
app.secret_key = 'dk9032ujr8923hf9eh23f3g279rfg12379gfg239uifh912uhf91uh9r12hfu1f29'
app.port = int(os.environ.get('PORT', 5000))

from app import routes
from app import optimusform
