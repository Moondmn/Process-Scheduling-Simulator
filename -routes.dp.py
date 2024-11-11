import copy
import pprint
from flask import Blueprint, jsonify, render_template, request
from concurrent.futures import ProcessPoolExecutor
from app.schedulers import (
    fcfs,
    hrrn,
    priority,
    # priority_p,
    rr,
    spn,
    srtf,
    sjn,
    # srtf_preemptive_quantum,
)
from app.utils import Process, handle_req

# Create a Blueprint instance
main = Blueprint("main", __name__)


def handle_single_scheduler(processes, scheduler, quantom_time=None, context_time=None):
    selected_process = scheduler.get(process)
    if scheduler in ["rr"]:
        return selected_process(processes, quantom_time, context_time)
    else:
        return selected_process(processes, context_time)


def handle_schedulers_parallel(scheduler, processes, quantom_time, context_time):
    processes_copy = copy.deepcopy(processes)
    schedulers = {
        "fcfs": fcfs,
        "hrrn": hrrn,
        "pr": priority,
        # "pr_0": priority_p,
        "rr": rr,
        "spn": spn,
        "srtf": srtf,
        "sjn": sjn,
    }

    with ProcessPoolExecutor() as executor:
        results = list(
            executor.map(
                handle_single_scheduler,
                [processes_copy] * len(schedulers),
                schedulers.values(),
                [quantom_time] * len(schedulers),
                [context_time] * len(schedulers),
            )
        )

    compared = []
    for i, result in enumerate(results):
        compare_TT, compare_WT, compare_FT = [], [], []
        for j in range(len(processes)):
            compare_TT.append(result["solved_processes_info"][j].turnaround_time)
            compare_WT.append(result["solved_processes_info"][j].waiting_time)
            compare_FT.append(result["solved_processes_info"][j].finish_time)
        _len = len(processes)
        avg_tt = sum(compare_TT) / _len
        avg_wt = sum(compare_WT) / _len
        avg_ft = sum(compare_FT) / _len
        compared.append(
            {list(schedulers.keys())[i]: {"tt": avg_tt, "wt": avg_wt, "ft": avg_ft}}
        )

    return compared


def handle_schedulers(processes, scheduler, quantom_time, context_time):
    v = handle_single_scheduler(processes, scheduler, quantom_time, context_time)

    if compare == "1":
        compared = handle_schedulers_parallel(
            scheduler, processes, quantom_time, context_time
        )

        # Sort based on turnaround time (tt)
        sorted_tt = sorted(
            enumerate(compared), key=lambda x: x[1][next(iter(x[1]))]["tt"]
        )
        # Sort based on waiting time (wt)
        sorted_wt = sorted(
            enumerate(compared), key=lambda x: x[1][next(iter(x[1]))]["wt"]
        )
        # Sort based on finish time (ft)
        sorted_ft = sorted(
            enumerate(compared), key=lambda x: x[1][next(iter(x[1]))]["ft"]
        )
        # Sort based on tt, wt, and ft
        sorted_algorithms = sorted(
            enumerate(compared),
            key=lambda x: (
                x[1][next(iter(x[1]))]["tt"],
                x[1][next(iter(x[1]))]["wt"],
                x[1][next(iter(x[1]))]["ft"],
            ),
        )

        # Extract sorted algorithm names and ranks
        sorted_algorithm_names_with_rank = [
            (index + 1, next(iter(algorithm_data)))
            for index, algorithm_data in sorted_algorithms
        ]

        cc = {
            "sorted_algos": sorted_algorithm_names_with_rank,
            "tt": sorted_tt,
            "wt": sorted_wt,
            "ft": sorted_ft,
        }
        return v, cc

    return v, None


# ... (rest of the code remains unchanged)


# Define a route and a corresponding view function
@main.route("/")
def home():
    return render_template("index.html")


@main.route("/pdata", methods=["POST"])
def prdata():
    print(request)
    process = handle_req(request)
    print(process)
    # output = handle_schedulers(
    #     process["algo"],
    #     process["process"],
    #     process["q_time"],
    #     process["context_time"],
    #     process["compare"],
    # )
    # scheduler_output = fcfs(process)
    # scheduler_output = fcfs(process)
    # print(scheduler_output)
    # req_v = req.values()
    # req_k = req.keys()
    # print(req["selectedOption"])
    # if req["selectedOption"] == "option1":
    #     sched_list = []
    #     for i in range()
    #     sched = fcfs

    # for k, v in req.items():
    #     print(v)
    # if d['selectedOption'] == 'FCFS':
    #     fcfs(input_data)
    # pprint.pprint(output)
    return jsonify({"output": 'output[0], "compared": output[1]'})
