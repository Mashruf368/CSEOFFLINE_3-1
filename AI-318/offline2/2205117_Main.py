from Graph import Graph
from Algorithm import greedy,semi_greedy,local_search,grasp
import csv
from known_best import known_best

alpha = 0.3
iterations = 10
print("=" * 70)
print("MAX-CUT Benchmark Evaluation")
print("=" * 70)

with open("2205117.csv", "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "Name",
        "|V|",
        "|E|",
        "Randomized",
        "Greedy",
        "Semi-Greedy",
        "Local Search Iterations",
        "Local Search Average Value",
        "GRASP Iterations",
        "GRASP Best Value",
        "Known Best Solution"
    ])

    for i in range(1, 55):

        filename = f"graphs/g{i}.rud"

        print("\n" + "=" * 70)
        print(f"Processing G{i}")
        print("=" * 70)

        try:
            graph = Graph.load_graph(filename)
        except Exception as e:
            print("Could not load", filename)
            print(e)
            continue

        print(f"Vertices : {graph.vertices}")
        print(f"Edges    : {graph.edges}")

        print("Running Randomized...")
        randomized_value = graph.randomized(iterations)
        print("Done.")

        print("Running Greedy...")
        _, greedy_value = greedy(graph)
        print("Done.")

        print("Running Semi-Greedy...")
        partition, semi_value = semi_greedy(graph, alpha)
        print("Done.")

        print("Running Local Search...")
        _, local_value, local_iterations = local_search(graph, partition)
        print("Done.")

        print("Running GRASP...")
        _, grasp_value, grasp_iterations = grasp(
            graph,
            iterations,
            alpha
        )
        print("Done.")

        print("\nSummary")
        print("------------------------------")
        print(f"Randomized : {randomized_value:.2f}")
        print(f"Greedy     : {greedy_value}")
        print(f"SemiGreedy : {semi_value}")
        print(f"Local      : {local_value}")
        print(f"GRASP      : {grasp_value}")

        writer.writerow([
            f"G{i}",
            graph.vertices,
            graph.edges,
            randomized_value,
            greedy_value,
            semi_value,
            local_iterations,
            local_value,
            grasp_iterations,
            grasp_value,
            known_best.get(f"G{i}", "")
        ])

        print("Written to CSV.")

print("\n")
print("=" * 70)
print("Finished processing all graphs.")
print("CSV saved as 2205117.csv")
print("=" * 70)