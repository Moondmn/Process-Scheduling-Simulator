# from dataclasses import dataclass, field
import pprint
from app.utils import Process


def priority(processes: list[Process], context_switch_time: int = 0) -> dict:
    current_time = 0
    processes_info = sorted(processes, key=lambda x: (x.arrival_time, -x.priority))
    solved_processes_info = []
    gantt_chart_info = []

    while processes_info:
        eligible_processes = [
            p for p in processes_info if p.arrival_time <= current_time
        ]
        if not eligible_processes:
            current_time += 1
            continue

        next_process = max(eligible_processes, key=lambda x: x.priority)

        if gantt_chart_info and context_switch_time is not None:
            current_time += context_switch_time

        start_time = current_time
        current_time += next_process.burst_time

        gantt_chart_info.append(
            {
                "job": next_process.name,
                "gantt_seq": [(start_time, current_time)],
            }
        )

        next_process.turnaround_time = current_time - next_process.arrival_time
        next_process.waiting_time = (
            next_process.turnaround_time - next_process.burst_time
        )
        next_process.finish_time = current_time

        solved_processes_info.append(next_process)
        processes_info.remove(next_process)

    solved_processes_info.sort(key=lambda x: (x.arrival_time, x.name))

    return {
        "solved_processes_info": solved_processes_info,
        "gantt_chart_info": gantt_chart_info,
    }


# Example usage with context switch time:
if __name__ == "__main__":
    processes = [
        Process(name="P1", arrival_time=0, burst_time=5, priority=3),
        Process(name="P2", arrival_time=10, burst_time=4, priority=2),
        Process(name="P3", arrival_time=2, burst_time=2, priority=1),
        Process(name="P4", arrival_time=3, burst_time=1, priority=4),
    ]

    context_switch_time = 2  # Change this value as needed

    result = priority(processes, context_switch_time)
    pprint.pprint(result)
