import json
import numpy as np
import pprint
from flask import Blueprint, jsonify, render_template, request
from multiprocessing import Pool, Manager
from app.schedulers import fcfs, hrrn, priority, rr, spn, srtf, sjn
from app.utils import Process, handle_req

# Create a Blueprint instance
main = Blueprint("main", __name__)


def run_scheduler(args):
    scheduler, processes, quantom_time, context_time = args
    v = None
    selected_process = scheduler

    if scheduler.__name__ == "rr":
        v = selected_process(processes, quantom_time, context_time)
    else:
        v = selected_process(processes, context_time)

    compare_TT, compare_WT, compare_FT = [], [], []

    for i in range(len(processes)):
        compare_TT.append(v["solved_processes_info"][i].turnaround_time)
        compare_WT.append(v["solved_processes_info"][i].waiting_time)
        compare_FT.append(v["solved_processes_info"][i].finish_time)

    _len = len(processes)
    avg_tt = sum(compare_TT) / _len
    avg_wt = sum(compare_WT) / _len
    avg_ft = sum(compare_FT) / _len

    return {
        "scheduler_name": scheduler.__name__,
        "tt": avg_tt,
        "wt": avg_wt,
        "ft": avg_ft,
    }


def handle_schedulers(schedulers, processes, quantom_time, context_time, compare):
    processes = np.array(processes)  # Convert to NumPy array for efficient operations
    manager = Manager()

    # Use manager.dict() for results instead of Pool
    result_dict = manager.dict()

    # Use a regular Pool for parallel processing
    with Pool() as pool:
        results = pool.map(
            run_scheduler,
            [
                (scheduler, processes, quantom_time, context_time)
                for scheduler in schedulers
            ],
        )

    # Convert results to a regular dictionary
    for result in results:
        result_dict[result["scheduler_name"]] = result
    # result_dict_to_json = json.dumps(result_dict.copy())
    print(result_dict)
    compared = result_dict.values()
    if compare == "1":
        # Sort based on turnaround time (tt)
        sorted_tt = sorted(enumerate(compared), key=lambda x: x[1]["tt"])
        # Sort based on waiting time (wt)
        sorted_wt = sorted(enumerate(compared), key=lambda x: x[1]["wt"])
        # Sort based on finish time (ft)
        sorted_ft = sorted(enumerate(compared), key=lambda x: x[1]["ft"])
        # Sort based on overall criteria (tt, wt, ft)
        sorted_algorithms = sorted(
            enumerate(compared),
            key=lambda x: (x[1]["tt"], x[1]["wt"], x[1]["ft"]),
        )

        # Extract sorted algorithm names and ranks
        sorted_algorithm_names_with_rank = [
            (index + 1, algorithm_data["scheduler_name"])
            for index, algorithm_data in sorted_algorithms
        ]

        return list(compared), {
            "sorted_algos": sorted_algorithm_names_with_rank,
            "tt": sorted_tt,
            "wt": sorted_wt,
            "ft": sorted_ft,
        }

    return list(compared), None


# Define a route and a corresponding view function
@main.route("/")
def home():
    return render_template("index.html")


@main.route("/pdata", methods=["POST"])
def prdata():
    process = handle_req(request)
    schedulers = [fcfs, hrrn, priority, rr, spn, srtf, sjn]
    output = handle_schedulers(
        schedulers,
        process["process"],
        process["q_time"],
        process["context_time"],
        process["compare"],
    )
    pprint.pprint(output)
    return jsonify({"output": output[0], "compared": output[1]})
