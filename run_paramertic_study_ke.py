from os import path
from os.path import join as pjoin
import numpy as nm
import matplotlib.pyplot as plt
import subprocess as sub

from PyFoam.Execution.AnalyzedRunner import AnalyzedRunner
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.Execution.UtilityRunner import UtilityRunner
from PyFoam.RunDictionary.ParameterFile import ParameterFile

from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Vector

from load_surface_data import load_raw_postdata

solver = "pisoFoam"
base_case_name = "base"

template_case = SolutionDirectory(base_case_name, archive=None, paraviewLink=False)


epsilons = nm.linspace(0, 3, 13)
nus = nm.ones(epsilons.shape) * 1e-6
for i, eps in enumerate(epsilons):
    case = template_case.cloneCase("testCase{:02}".format(i))

    epsilonBC = ParsedParameterFile(path.join(case.name, "0", "epsilon"))
    epsilonBC["boundaryField"]["inletBoundary_patch0"]["value"].setUniform(eps)
    epsilonBC.writeFile()
    # epsilonBC.closeFile()

    run = BasicRunner(argv=[solver, "-case", case.name], silent=False)
    run.start()

    case = SolutionDirectory(case.name, archive=None, paraviewLink=False)

    if float(max(case.times)) < .28:
        case.clear()
        case.clearResults()
        trans = ParameterFile(path.join(case.name, "constant/transportProperties"))
        trans.readFile()
        trans.replaceParameter("nu", "[0 2 -1 0 0 0 0]  1e-5")
        trans.writeFile()
        # trans.closeFile()
        nus[i] = 1e-5
        run = BasicRunner(argv=[solver, "-case", case.name], silent=False)
        run.start()

    post = UtilityRunner("postProcess -func surfaces".split(" ") + ['-case', case.name])
    post.start()

    p_top, p_bot, _ = load_raw_postdata(case.name, time="last")
    p_top = p_top[0]
    p_bot = p_bot[0]

    fig, ax = plt.subplots()
    ax.plot(range(len(p_top)), p_bot, label="bot")
    ax.plot(range(len(p_top)), p_top, label="top")

    fig.savefig(pjoin(path.basename(case.name), "p_top_bot_129.png"))

epsilons.tofile("epsilons.txt", sep=";")
nus.tofile("nus.txt", sep=";")






