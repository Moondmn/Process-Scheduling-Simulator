from collections import defaultdict
from dataclasses import dataclass, field
import pprint
from app.utils import compress_sequence, uniqify, group_dict_value, Process


def sjn(
    processes: list[Process], context_switch_time: int = 0
) -> dict:
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

        next_process = min(eligible_processes, key=lambda x: x.remaining_time)
        remaining_time = next_process.remaining_time

        # Include context switch time
        # if current_time is not None:
        current_time += context_switch_time

        gantt_chart_info.append(
            {
                "job": next_process.name,
                "gantt_seq": [
                    (current_time, (current_time := current_time + remaining_time)),
                ],
            }
        )
        # Set finish_time
        next_process.finish_time = current_time
        next_process.remaining_time = 0
        next_process.turnaround_time = current_time - next_process.arrival_time
        next_process.waiting_time = (
            next_process.turnaround_time - next_process.burst_time
        )

        solved_processes_info.append(next_process)
        processes_info.remove(next_process)

    return {
        "solved_processes_info": solved_processes_info,
        "gantt_chart_info": gantt_chart_info,
    }


# Example usage with context switch time:
if __name__ == "__main__":
    processes = [
        Process(name="P1", arrival_time=0, burst_time=3),
        Process(name="P2", arrival_time=2, burst_time=6),
        Process(name="P3", arrival_time=4, burst_time=4),
        Process(name="P4", arrival_time=6, burst_time=5),
        Process(name="P5", arrival_time=8, burst_time=2),
    ]

    context_switch_time = 2  # Change this value as needed

    result = srtf(processes, context_switch_time)
    pprint.pprint(result)
