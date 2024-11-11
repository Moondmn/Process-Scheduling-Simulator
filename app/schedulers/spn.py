from dataclasses import dataclass, field
import pprint
from app.utils import group_dict_value, Process


def spn(
    processes: list[Process], context_switch_time: int = 0
) -> tuple:
    processes_info = sorted(processes, key=lambda p: (p.arrival_time, p.burst_time))

    solved_processes_info = []
    gantt_chart_info = []

    current_time = 0

    while processes_info:
        ready_processes = [p for p in processes_info if p.arrival_time <= current_time]

        if not ready_processes:
            # No ready processes, move time to the next arrival
            current_time = processes_info[0].arrival_time
        else:
            # Select the process with the shortest burst time
            process_to_execute = min(ready_processes, key=lambda p: p.burst_time)

            remaining_t = process_to_execute.burst_time
            process_to_execute.burst_time = 0
            prev_current_time = current_time
            current_time += remaining_t

            gantt_chart_info.append(
                {
                    "job": process_to_execute.name,
                    "gantt_seq": [(prev_current_time, current_time)],
                }
            )

            process_to_execute.finish_time = current_time
            process_to_execute.turnaround_time = (
                current_time - process_to_execute.arrival_time
            )
            process_to_execute.waiting_time = (
                process_to_execute.turnaround_time - process_to_execute.burst_time
            )

            solved_processes_info.append(process_to_execute)
            processes_info.remove(process_to_execute)

            # Add context switch time to the current time
            current_time += context_switch_time

    return {
        "solved_processes_info": solved_processes_info,
        "gantt_chart_info": gantt_chart_info,
    }


# Example Usage:
if __name__ == "__main__":
    processes_list = [
        Process(name="P1", arrival_time=0, burst_time=8),
        Process(name="P2", arrival_time=2, burst_time=1),
        Process(name="P3", arrival_time=2, burst_time=4),
        # Add more processes as needed
    ]

    # Example usage with context switch time
    spn_result = spn(processes_list, context_switch_time=1)
    pprint({"solved_processes_info": spn_result[0], "gantt_chart_info": spn_result[1]})
