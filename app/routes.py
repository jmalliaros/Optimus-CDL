from flask import render_template, jsonify
from app import app
import app.optimusform as opform

@app.route('/')
def compute():
    return render_template('base.html')

@app.route('/submit_program')
def submit_program():
    return jsonify({"results_block": render_template("results_block.html"), "status": "success"})

