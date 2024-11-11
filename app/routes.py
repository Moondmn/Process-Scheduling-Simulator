import copy
import concurrent.futures
import pprint
import numpy as np

# from app import setup_logging
import logging

# from app import create_app
from flask import Blueprint, jsonify, render_template, request, current_app
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
import timeit

# Create a Blueprint instance
main = Blueprint("main", __name__)
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# setup_logging(current_app)


def run_scheduler_parallel(scheduler_func, processes, quantom_time, context_time):
    # processes_copy = copy.deepcopy(processes)
    scheduler_to_run: Process = None
    start_time = timeit.default_timer()
    if scheduler_func.__name__ in ["rr"]:
        scheduler_to_run = scheduler_func(processes, quantom_time, context_time)
    else:
        scheduler_to_run = scheduler_func(processes, context_time)
    execution_time = timeit.default_timer() - start_time
    avg_extime_tt_wt_ft = {
        scheduler_func.__name__: [
            execution_time,
            *[
                sum_column / len(scheduler_to_run["solved_processes_info"])
                for sum_column in np.sum(
                    np.array(
                        [
                            [
                                p.turnaround_time,
                                p.waiting_time,
                                p.finish_time,
                            ]
                            for p in scheduler_to_run["solved_processes_info"]
                        ]
                    ),
                    axis=0,
                )
            ],
        ]
    }
    return {
        "AlgoResult": scheduler_to_run,
        "avg": avg_extime_tt_wt_ft,
        "name": scheduler_func.__name__,
    }


def handle_schedulers_compare(processes_list, quantom_time, context_time, _len):
    # Rest of your code for comparisons and results

    schedulers = [fcfs, hrrn, rr, spn, srtf, sjn]
    args = [
        (scheduler, processes_list, quantom_time, context_time)
        for scheduler in schedulers
    ]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # resualt = executer.map(lambda x: run_scheduler_parallel(*x), args)
        handled_schedulers = [
            executor.submit(
                run_scheduler_parallel,
                scheduler,
                processes_list,
                quantom_time,
                context_time,
            )
            for scheduler in schedulers
        ]
        schedulers_results = {}
        avg_extime_tt_wt_fts = []
        for handled_scheduler in concurrent.futures.as_completed(handled_schedulers):
            try:
                result = handled_scheduler.result()
                current_app.logger.info(f'Running {result["avg"]}')
                avg_extime_tt_wt_fts.append(result["avg"])
                schedulers_results |= {result["name"]: result["AlgoResult"]}
            except Exception as e:
                current_app.logger.error(f"Error: {e}")

    current_app.logger.info(f"End:")

    return schedulers_results, avg_extime_tt_wt_fts


def handle_schedulers(scheduler, processes, quantom_time, context_time, compare, _len):
    processes_copy = copy.deepcopy(processes)

    if compare == "0":
        schedulers = {
            "fcfs": fcfs,
            "hrrn": hrrn,
            "pr": priority,
            "rr": rr,
            "spn": spn,
            "srtf": srtf,
            "sjn": sjn,
        }
        simple_evaluation = None
        selected_process = schedulers.get(scheduler)
        # print(selected_process)
        if scheduler in ["rr"]:
            simple_evaluation = selected_process(processes, quantom_time, context_time)
        else:
            simple_evaluation = selected_process(processes, context_time)
        return simple_evaluation, None, "notReady"
    elif compare == "1":
        all_evaluations, avg_extime_tt_wt_fts = handle_schedulers_compare(
            processes_copy, quantom_time, context_time, _len
        )
        return all_evaluations, avg_extime_tt_wt_fts, "Ready"


# Define a route and a corresponding view function
@main.route("/")
def home():
    return render_template("index.html")


@main.route("/pdata", methods=["POST"])
def prdata():
    print(request)
    process = handle_req(request)
    evaluation, avgs, ready_handler = handle_schedulers(
        process["algo"],
        process["process"],
        process["q_time"],
        process["context_time"],
        process["compare"],
        process["length"],
    )
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
    return jsonify(
        {"evaluation": evaluation, "avgs": avgs, "readHandler": ready_handler}
    )
