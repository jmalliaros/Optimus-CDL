from flask import render_template
from app import app
import app.optimusform as opform

@app.route('/')
def compute():
    form = opform
    return render_template('base.html', form=form)
