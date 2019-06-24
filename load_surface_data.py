import numpy as nm
import pandas as pd
import matplotlib.pyplot as plt


import os
from os.path import join as pjoin
from glob import glob

postproc_path = "postProcessing/surfaces/"


def load_raw_postdata(case_folder, time, filepath_form=None):

    if filepath_form is None:
        filepath_form = "{time}/p_{pos}wall_constant.raw"

    if time in ["all", "last"]:
        times = (os.path.basename(t) for t in glob(pjoin(case_folder, postproc_path, "*")))
        print(glob(pjoin(case_folder, postproc_path, "*")))
        times = sorted(list(times))
        if time == "last":
            times = [times[-1]]
    else:
        times = [time]

    p_tops = []
    p_bots = []
    for time in times:

        filename_top = pjoin(case_folder, postproc_path, filepath_form.format(time=str(time), pos="top"))
        filename_bot = pjoin(case_folder, postproc_path, filepath_form.format(time=str(time), pos="bot"))

        df_top_p = pd.read_csv(filename_top, sep=" ", header=None, skiprows=[0, 1])
        df_bot_p = pd.read_csv(filename_bot, sep=" ", header=None, skiprows=[0, 1])

        p_top = df_top_p.sort_values(0)[3]
        p_bot = df_bot_p.sort_values(0)[3]

        p_tops.append(p_top)
        p_bots.append(p_bot)

    return nm.array(p_tops), nm.array(p_bots), nm.array(times, dtype=nm.float)


def load_cases(folder, case_name_regexp, time):
    case_folders = sorted(glob(pjoin(folder, case_name_regexp)))
    case_datas_top = []
    case_datas_bot = []
    ctimes = []
    for case in case_folders:
        if os.path.isdir(case):
            p_tops, p_bots, ctime = load_raw_postdata(case, time)
            case_datas_bot.append(p_bots)
            case_datas_top.append(p_tops)
            ctimes.append(ctime)

    return case_datas_top, case_datas_bot, ctimes


if __name__ == '__main__':
    p_top, p_bot, times, nums = load_cases(".", "*[Cc]ase*", "last")  # "*[Cc]ase_nowf[1-9]**"
    epsilons = nm.fromfile("epsilons.txt", sep=";")

    n_cases = len(p_top)

    # fig, ax = plt.subplots()
    # alpha = .1
    # case_n = 1
    # n_times = times[case_n].shape[0]
    # for n in range(n_times):
    #     alpha += 1 / n_times
    #     print(alpha)
    #     ax.plot(nm.arange(p_top[case_n].shape[1]), p_top[0][ n, :], alpha=alpha, color="Orange")
    #     ax.plot(nm.arange(p_bot[case_n].shape[1]), p_bot[0][ n, :], alpha=alpha, color="blue")

    fig, ax = plt.subplots()


    fig.suptitle("Per case pressure top")
    alpha = 1
    for n in range(n_cases):
        # alpha += 1 / n_cases
        print(alpha)
        p = ax.plot(nm.arange(p_top[n].shape[1]), p_top[n][-1, :], "--",
                alpha=alpha, label="Top {} t={}".format(epsilons[n], times[n][-1]))
        ax.plot(nm.arange(p_bot[n].shape[1]), p_bot[n][-1, :],
                alpha=alpha, label="Bot {} t={}".format(epsilons[n], times[n][-1]), color=p[0].get_color())
    fig.legend()
    plt.show()



