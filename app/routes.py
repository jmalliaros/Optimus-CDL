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
from stats_ibm import plot_this

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
    ibm_base64 = None
    try:
        res, shots, qubo, old_qubo, res_ibm, res_rig = route(program_string)
        base64 = get_dwave_plot(res).decode('utf8')
        base64_2 = get_networkx_plot_of_qubo(qubo, old_qubo).decode('utf8')

        if res_ibm:
            ibm_base64 = plot_this(res_ibm).decode('utf8')
        else:
            ibm_base64 = None


        if res_rig:
            rig_base64 = plot_this(res_rig).decode('utf8')
        else:
            rig_base64 = None

    except Exception:
        e = traceback.format_exc()
        print("dsadas", e)

    return jsonify({"results_block": render_template("results_block.html", e=e, shots=shots, ibm_base64=ibm_base64, result=base64, image_2=base64_2), "status": "success"})
