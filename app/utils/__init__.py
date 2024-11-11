from collections import defaultdict

from flask import Request
from .process import Process


def compress_sequence(input_list):
    result = []
    start = end = input_list[0]

    for num in input_list[1:]:
        if num == end + 1:
            end = num
        else:
            result.append((start, end))
            start = end = num

    result.append((start, end))
    return result


def group_dict_value(data):
    grouped_data = defaultdict(lambda: {"job": None, "gantt_seq": []})
    for item in data:
        job = item["job"]
        grouped_data[job]["job"] = job
        # grouped_data[job]["start"].append(item["start"])
        # grouped_data[job]["stop"].append(item["stop"])
        grouped_data[job]["gantt_seq"].append(item["gantt_seq"][0])
    return list(grouped_data.values())


def uniqify(_list):
    flat_list = sorted([item for sublist in _list for item in sublist])
    return list(set(flat_list))


def handle_req(req: Request):
    req_dict = req.form.to_dict()

    nums = int(req_dict["numRows"])

    process = [
        Process(
            name=i,
            arrival_time=int(req_dict[f"{i}-at"]),
            burst_time=int(req_dict[f"{i}-cbt"]),
            priority=int(req_dict[f"{i}-pr"]),
        )
        for i in range(1, nums + 1)
    ]

    return {
        "process": process,
        "algo": req_dict["selectedAlgo"],
        "q_time": int(req_dict["qTime"]),
        "context_time": int(req_dict["csTime"]),
        "compare": req_dict["compare"],
        "length": nums,
    }


__all__ = [Process, group_dict_value, compress_sequence, uniqify, handle_req]
