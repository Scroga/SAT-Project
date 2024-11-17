from argparse import ArgumentParser

def generate_complete_graph_edges(n):
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            edges.append((u, v))
    return edges

def print_to_file(nr_nodes, k, edges, output_name):
    is_requited = 1
    with open(output_name, "w") as file:
        file.write(str(nr_nodes) + "\n")
        file.write(str(k) + "\n")
        for i in range(0, len(edges)):
            u, v = edges[i]   
            file.write( str(u) + " " + str(v) +  " " + str(is_requited)) 
            # if(is_requited == 0): is_requited = 1
            # else: is_requited = 0
            if(i == len(edges) - 2): is_requited = 1
            else: is_requited = 0
            if(i != len(edges) - 1): file.write("\n")

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-n",
        "--nr_nodes",
        default="4",
        type=int,
        help=(
            "The number of vertices"
        ),
    )
    parser.add_argument(
        "-k",
        default="4",
        type=int,
        help=(
            "Max. cycle length"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="generated_graph.in",
        type=str,
        help=(
            "Output file contains the completed graph."
        ),
    )
    args = parser.parse_args()

    edges = generate_complete_graph_edges(args.nr_nodes)
    print_to_file(args.nr_nodes, args.k, edges, args.output)