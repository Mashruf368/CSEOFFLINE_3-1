import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

graphs = []
randomized = []
greedy = []
semi = []
local = []
grasp = []

with open("2205117.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        graphs.append(row["Name"])
        randomized.append(float(row["Randomized"]))
        greedy.append(float(row["Greedy"]))
        semi.append(float(row["Semi-Greedy"]))
        local.append(float(row["Local Search Average Value"]))
        grasp.append(float(row["GRASP Best Value"]))

pdf = PdfPages("Algorithm_Comparison_Plots.pdf")

graphs_per_page = 5

for start in range(0, len(graphs), graphs_per_page):

    end = min(start + graphs_per_page, len(graphs))

    g = graphs[start:end]
    r = randomized[start:end]
    gr = greedy[start:end]
    sg = semi[start:end]
    ls = local[start:end]
    gp = grasp[start:end]

    x = np.arange(len(g))
    width = 0.16

    plt.figure(figsize=(11,6))

    plt.bar(x-2*width, r, width, label="Randomized")
    plt.bar(x-width, gr, width, label="Greedy")
    plt.bar(x, sg, width, label="Semi-Greedy")
    plt.bar(x+width, ls, width, label="Local Search")
    plt.bar(x+2*width, gp, width, label="GRASP")

    plt.xticks(x, g)
    plt.xlabel("Benchmark Graph")
    plt.ylabel("Cut Value")
    plt.title(f"MAX-CUT Benchmark ({g[0]} - {g[-1]})")

    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.legend()

    plt.tight_layout()

    pdf.savefig()
    plt.close()

pdf.close()

print("Created Algorithm_Comparison_Plots.pdf")