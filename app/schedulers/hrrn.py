# from dataclasses import dataclass, field
import pprint
from app.utils import group_dict_value, Process


def hrrn(processes: list[Process], context_switch_time: int = 0) -> dict:
    current_time = 0
    processes_info = sorted(processes, key=lambda x: x.arrival_time)
    solved_processes_info = []
    gantt_chart_info = []

    while processes_info:
        eligible_processes = [
            p for p in processes_info if p.arrival_time <= current_time
        ]
        if not eligible_processes:
            current_time += 1
            continue

        hrr_values = [
            (p, (current_time - p.arrival_time + p.burst_time) / p.burst_time)
            for p in eligible_processes
        ]

        next_process = max(hrr_values, key=lambda x: x[1])[0]

        # Include context switch time
        current_time += context_switch_time

        gantt_chart_info.append(
            {
                "job": next_process.name,
                "gantt_seq": [
                    (
                        current_time,
                        (current_time := current_time + next_process.burst_time),
                    ),
                ],
            }
        )

        next_process.turnaround_time = current_time - next_process.arrival_time
        next_process.waiting_time = (
            next_process.turnaround_time - next_process.burst_time
        )

        # Set finish_time
        next_process.finish_time = current_time

        solved_processes_info.append(next_process)
        processes_info.remove(next_process)

    return {
        "solved_processes_info": solved_processes_info,
        "gantt_chart_info": gantt_chart_info,
    }


if __name__ == "__main__":
    # Example usage:
    processes = [
        Process(name="P1", arrival_time=0, burst_time=3),
        Process(name="P2", arrival_time=20, burst_time=6),
        Process(name="P3", arrival_time=4, burst_time=4),
        Process(name="P4", arrival_time=6, burst_time=5),
        Process(name="P5", arrival_time=8, burst_time=2),
    ]
    result = hrrn(processes)
    pprint.pprint(result)
