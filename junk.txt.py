# compared = []

# compare_TT = []
# compare_WT = []
# compare_FT = []

# # vp = selected_ps(a, quantom_time, context_time)
# for i in range(len(processes)):
#     compare_TT.append(simple_evaluation["solved_processes_info"][i].turnaround_time)
#     compare_WT.append(simple_evaluation["solved_processes_info"][i].waiting_time)
#     compare_FT.append(simple_evaluation["solved_processes_info"][i].finish_time)
# _len = len(processes)
# avg_tt = sum(compare_TT) / _len
# avg_wt = sum(compare_WT) / _len
# avg_ft = sum(compare_FT) / _len
# compared.append({scheduler: {"tt": avg_tt, "wt": avg_wt, "ft": avg_ft}})

# if compare == "1":
#     # print(processes_copy, "dfdhfjhv")
#     for p in schedulers.keys():
#         # print(p)
#         compare_TT = []
#         compare_WT = []
#         compare_FT = []
#         # print(selected_ps)
#         if p in ["pr"] or p in [scheduler]:
#             continue
#         # print(p, "dfbsjdfljsavdfjh")
#         selected_ps = schedulers.get(p)
#         if p in ["rr"]:
#             b = copy.deepcopy(processes_copy)
#             print(b)
#             vp = selected_ps(b, quantom_time, context_time)
#             for i in range(len(b)):
#                 compare_TT.append(vp["solved_processes_info"][i].turnaround_time)
#                 compare_WT.append(vp["solved_processes_info"][i].waiting_time)
#                 compare_FT.append(vp["solved_processes_info"][i].finish_time)
#             _len = len(processes)
#             avg_tt = sum(compare_TT) / _len
#             avg_wt = sum(compare_WT) / _len
#             avg_ft = sum(compare_FT) / _len
#             compared.append({p: {"tt": avg_tt, "wt": avg_wt, "ft": avg_ft}})
#             del b

#         else:
#             b = copy.deepcopy(processes_copy)
#             # print(b)
#             vp = selected_ps(b, context_time)
#             for i in range(len(b)):
#                 compare_TT.append(vp["solved_processes_info"][i].turnaround_time)
#                 compare_WT.append(vp["solved_processes_info"][i].waiting_time)
#                 compare_FT.append(vp["solved_processes_info"][i].finish_time)
#             _len = len(processes)
#             avg_tt = sum(compare_TT) / _len
#             avg_wt = sum(compare_WT) / _len
#             avg_ft = sum(compare_FT) / _len
#             compared.append({p: {"tt": avg_tt, "wt": avg_wt, "ft": avg_ft}})
#             del b

#         sorted_tt = sorted(
#             enumerate(compared), key=lambda x: x[1][next(iter(x[1]))]["tt"]
#         )
#         # Sort based on waiting time (wt)
#         sorted_wt = sorted(
#             enumerate(compared), key=lambda x: x[1][next(iter(x[1]))]["wt"]
#         )
#         # Sort based on finish time (ft)
#         sorted_ft = sorted(
#             enumerate(compared), key=lambda x: x[1][next(iter(x[1]))]["ft"]
#         )

#         # Calculate the weighted average for each process
#         weighted_avg = []
#         weight_tt = 2
#         weight_wt = 1
#         weight_ft = 2
#         for i in range(len(compared)):
#             p = next(iter(compared[i]))
#             weighted_tt = weight_tt * compared[i][p]["tt"]
#             weighted_wt = weight_wt * compared[i][p]["wt"]
#             weighted_ft = weight_ft * compared[i][p]["ft"]
#             total_weighted_avg = weighted_tt + weighted_wt + weighted_ft
#             weighted_avg.append((i, p, total_weighted_avg))

#     # Sort based on the total weighted average
#     sorted_weighted = sorted(weighted_avg, key=lambda x: x[2])
#     cc = (
#         simple_evaluation,
#         {
#             "sorted_algos": sorted_weighted,
#             "tt": sorted_tt,
#             "wt": sorted_wt,
#             "ft": sorted_ft,
#         },
#     )
#     return cc
# cc = (simple_evaluation, None)
# return cc
