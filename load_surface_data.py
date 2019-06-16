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

    return nm.array(p_tops), nm.array(p_bots), nm.array(times)


def load_cases(folder, case_name_regexp, time):
    case_folders = glob(pjoin(folder, case_name_regexp))
    case_datas_top = []
    case_datas_bot = []
    for case in case_folders:
        if os.path.isdir(case):
            p_tops, p_bots, times = load_raw_postdata(case, time)
            case_datas_bot.append(p_bots)
            case_datas_top.append(p_tops)

    p_top = nm.stack(case_datas_top)
    p_bot = nm.array(case_datas_bot)

    return p_top, p_bot, times


if __name__ == '__main__':
    p_top, p_bot, times = load_cases(".", "*[Cc]ase_nowf*", "last")

    # fig, ax = plt.subplots()
    # alpha = .1
    # for n in range(p_top.shape[1]//10):
    #     alpha += 1/(p_top.shape[1]//10)
    #     print(alpha)
    #     ax.plot(nm.arange(p_top.shape[2]), p_top[0, n*10, :], alpha=alpha, color="Orange")
    #     ax.plot(nm.arange(p_bot.shape[2]), p_bot[0, n*10, :], alpha=alpha, color="blue")

    fig, ax = plt.subplots()
    alpha = .1
    for n in range(p_top.shape[0]):
        alpha += 1 / (p_top.shape[1])
        print(alpha)
        ax.plot(nm.arange(p_top.shape[2]), p_top[n, -1, :], alpha=alpha, color="Orange")
        ax.plot(nm.arange(p_bot.shape[2]), p_bot[n, -1, :], alpha=alpha, color="blue")

    plt.show()



