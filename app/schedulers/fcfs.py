# from utils.process import Process
# from app.utils import uniqify, compress_sequence, Process


from dataclasses import dataclass, field
import pprint
from app.utils import Process


def fcfs(processes: list[Process], context_switch_time: int = 0) -> dict:
    current_time = 0
    processes_info = sorted(processes, key=lambda x: x.arrival_time)
    solved_processes_info = []
    gantt_chart_info = []

    for process in processes_info:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        gantt_chart_info.append(
            {
                "job": process.name,
                "gantt_seq": [
                    (current_time, (current_time := current_time + process.burst_time)),
                ],
            }
        )

        # Include context switch time
        current_time += context_switch_time

        process.turnaround_time = current_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        # Set finish_time
        process.finish_time = current_time

        solved_processes_info.append(process)

    return {
        "solved_processes_info": solved_processes_info,
        "gantt_chart_info": gantt_chart_info,
    }


if __name__ == "__main__":
    # Example usage:
    processes = [
        Process(name="P1", arrival_time=0, burst_time=5, priority=3),
        Process(name="P2", arrival_time=10, burst_time=4, priority=2),
        Process(name="P3", arrival_time=2, burst_time=2, priority=1),
        Process(name="P4", arrival_time=3, burst_time=1, priority=4),
    ]
    result = fcfs(processes)
    pprint.pprint(result)
