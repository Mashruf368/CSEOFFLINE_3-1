import csv
import matplotlib.pyplot as plt

graphs = []
randomized_results = []
greedy_results = []
semi_results = []
local_results = []
grasp_results = []

with open("2205117.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        graphs.append(row["Name"])
        randomized_results.append(float(row["Randomized"]))
        greedy_results.append(float(row["Greedy"]))
        semi_results.append(float(row["Semi-Greedy"]))
        local_results.append(float(row["Local Search Avaerage Value"]))
        grasp_results.append(float(row["GRASP Best Value"]))

plt.figure(figsize=(14, 7))

plt.plot(graphs, randomized_results, marker='o', label="Randomized")
plt.plot(graphs, greedy_results, marker='s', label="Greedy")
plt.plot(graphs, semi_results, marker='^', label="Semi-Greedy")
plt.plot(graphs, local_results, marker='d', label="Local Search")
plt.plot(graphs, grasp_results, marker='*', label="GRASP")

plt.xlabel("Benchmark Graph")
plt.ylabel("Cut Value")
plt.title("Comparison of MAX-CUT Algorithms")
plt.xticks(rotation=90)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("comparison.png", dpi=300)
plt.show()