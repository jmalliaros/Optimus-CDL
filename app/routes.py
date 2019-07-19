import matplotlib
matplotlib.use("Agg")

import traceback
from flask import render_template, jsonify, request
from app import app
import app.optimusform as opform
import sys
sys.path.append("..")
from hardware_router import route
from stats import get_dwave_plot, get_networkx_plot_of_qubo
from optimus_parser import refresh_globals

@app.route('/')
def compute():
    return render_template('base.html')

@app.route('/submit_program', methods=['POST'])
def submit_program():
    program_string = request.form['program_string']
    refresh_globals()
    e = None
    base64 = None
    shots = None
    base64_2 = None
    try:
        res, shots, qubo, old_qubo = route(program_string)
        base64 = get_dwave_plot(res).decode('utf8')
        base64_2 = get_networkx_plot_of_qubo(qubo, old_qubo).decode('utf8')
    except Exception:
        e = traceback.format_exc()
        print("dsadas", e)

    return jsonify({"results_block": render_template("results_block.html", e=e, shots=shots, result=base64, image_2=base64_2), "status": "success"})
