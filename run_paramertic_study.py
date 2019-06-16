from os import path
from os.path import join as pjoin
import numpy as nm
import matplotlib.pyplot as plt
import subprocess as sub

from PyFoam.Execution.AnalyzedRunner import AnalyzedRunner
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.Execution.UtilityRunner import UtilityRunner

from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector

from load_surface_data import load_raw_postdata



solver = "pisoFoam"
base_case = "base_nowf"

templateCase = SolutionDirectory(base_case, archive=None, paraviewLink=False)


epsilons = nm.linspace(0, 3, 13)
epsilons.tofile("epsilons.txt", sep=";")

for i, eps in enumerate(epsilons):
    case = templateCase.cloneCase("testCase_nowf" + str(i))

    epsilonBC = ParsedParameterFile(path.join(case.name, "0", "epsilon"))
    epsilonBC["boundaryField"]["fixedWalltop_patch1"]["value"].setUniform(eps)
    epsilonBC["boundaryField"]["fixedWallbot_patch1"]["value"].setUniform(eps)
    epsilonBC.writeFile()
    # sub.run([solver, "-case", case.name])
    run = BasicRunner(argv=[solver, "-case", case.name], silent=False)
    run.start()
    post = UtilityRunner("postProcess -func surfaces".split(" ") + ['-case', case.name])
    post.start()

    p_top, p_bot, _ = load_raw_postdata(case.name, time="last")

    fig, ax = plt.subplots()
    ax.plot(range(len(p_top)), p_bot, label="bot")
    ax.plot(range(len(p_top)), p_top, label="top")

    fig.savefig(pjoin(path.basename(case.name), "p_top_bot_129.png"))




