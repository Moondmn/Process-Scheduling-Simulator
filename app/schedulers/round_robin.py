# from app.utils import uniqify, compress_sequence, Process


from collections import defaultdict


from dataclasses import dataclass, field
import pprint
from app.utils import group_dict_value, Process


def rr(
    processes: list[Process], time_quantum: int, context_switch_time: int = 0
) -> dict:
    processes_info = sorted(processes, key=lambda x: x.arrival_time)
    solved_processes_info = []
    gantt_chart_info = []

    ready_queue = []
    current_time = processes_info[0].arrival_time
    unfinished_jobs = processes_info.copy()

    while (
        any(process.remaining_time > 0 for process in processes_info)
        and unfinished_jobs
    ):
        if not ready_queue and unfinished_jobs:
            ready_queue.append(unfinished_jobs[0])
            current_time = ready_queue[0].arrival_time

        process_to_execute = ready_queue[0]

        remaining_t = min(process_to_execute.remaining_time, time_quantum)
        process_to_execute.remaining_time -= remaining_t

        gantt_chart_info.append(
            {
                "job": process_to_execute.name,
                "gantt_seq": [
                    (current_time, (current_time := current_time + remaining_t)),
                ],
            }
        )

        process_to_arrive_in_this_cycle = [
            p
            for p in processes_info
            if p.next_arrival_time <= current_time
            and p != process_to_execute
            and p not in ready_queue
            and p in unfinished_jobs
        ]

        ready_queue.extend(process_to_arrive_in_this_cycle)
        ready_queue.append(ready_queue.pop(0))

        # Include context switch time
        current_time += context_switch_time

        if process_to_execute.remaining_time == 0:
            unfinished_jobs.remove(process_to_execute)
            ready_queue.remove(process_to_execute)

            process_to_execute.turnaround_time = (
                current_time - process_to_execute.arrival_time
            )
            process_to_execute.waiting_time = (
                process_to_execute.turnaround_time - process_to_execute.burst_time
            )

            # Set finish_time
            process_to_execute.finish_time = current_time

            solved_processes_info.append(process_to_execute)

    solved_processes_info.sort(key=lambda x: (x.arrival_time, x.name))

    return {
        "solved_processes_info": solved_processes_info,
        "gantt_chart_info": group_dict_value(gantt_chart_info),
    }


# Example usage:
# processes = [
#     Process(name="P1", arrival_time=0, burst_time=5),
#     Process(name="P2", arrival_time=1, burst_time=4),
#     Process(name="P3", arrival_time=2, burst_time=2),
#     Process(name="P4", arrival_time=3, burst_time=1),
# ]
if __name__ == "__main__":
    processes = [
        Process(name="P1", arrival_time=0, burst_time=5),
        Process(name="P2", arrival_time=10, burst_time=4),
        Process(name="P3", arrival_time=2, burst_time=2),
        Process(name="P4", arrival_time=3, burst_time=1),
    ]
    time_quantum = 2
    result = rr(processes, time_quantum)
    pprint.pprint(result)
