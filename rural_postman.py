import subprocess
from argparse import ArgumentParser

DEBUG = False

def load_instance(input_file_name):
    # read the input instance
    global VERTICES, EDGES
    VERTICES = []
    EDGES = []
    required_edges = set()

    with open(input_file_name, "r") as file:
        nr_vertices = int(next(file))    # first line is the number of vertices in graph 
        k = int(next(file))           # second line is the maximum number of edges that will contain the cycle 

        for line in file:             # other lines contain the edges
            v1, v2, required = line.split()
            edge = (int(v1), int(v2))

            EDGES.append(edge)
            if int(required) == 1:    # add required edges (subset F)
                required_edges.add(edge)
    
    return (required_edges, k)

def combinations(iterable, r):
    def combinations_helper(start, current_comb):
        if len(current_comb) == r:
            result.append(current_comb)
            return

        for i in range(start, len(iterable)):
            combinations_helper(i + 1, current_comb + [iterable[i]])
    result = []
    combinations_helper(0, [])
    return result

def get_neighbors(edge):
    neighbors = []
    for other_edge in EDGES:
        if edge != other_edge and (edge[0] in other_edge or edge[1] in other_edge):
            neighbors.append(other_edge)
    return neighbors

def print_cnf(cnf):
    if DEBUG:
        for clause in cnf:
            print(f"{clause} \n")

def encode(instance):
    # given the instance, create a cnf formula, i.e. a list of lists of integers
    # also return the total number of variables used

    # each edge in the graph has a variable that indicates whether or not the edge is in cycle
    # each variable is represented by an integer, varaibles are numbered from 1

    required_edges, k = instance
    cnf = []
    
    # create variables for edges 
    # variable i corresponds to edge i in the graph being part of the solution
    edge_to_var = {edge: i + 1 for i, edge in enumerate(EDGES)}
    variables = list(edge_to_var.values())
    nr_vars = len(variables)

    # each required edge must be included in cnf
    if DEBUG : cnf.append("Add required edges")
    if len(required_edges) > 0:
        for edge in required_edges:
            if edge in edge_to_var:
                cnf.append([edge_to_var[edge], 0])

    # generate clauses to ensure no more than k edges are in cycle
    # we do this by adding clauses that prevent any combination of k + 1 edges from all being True
    if DEBUG : cnf.append("Prevent any combination of k + 1 edges")
    if nr_vars > k:
        for i in range(k + 1, len(EDGES) + 1):
            for comb in combinations(variables, i):
                clause = [ -var for var in comb]
                cnf.append(clause + [0])

    # ensures local connectivity
    # if an edge is included in a cycle, at least two of its neighbors must also be included
    if DEBUG : cnf.append("At least two neighbors")
    for edge in EDGES:
        neighbors = [ edge_to_var[neighbor] for neighbor in get_neighbors(edge)]
        edge_var = edge_to_var[edge]

        if len(neighbors) == 2:
            # for edges with exactly two neighbors, both neighbors must be included if the edge is included
                cnf.append([-edge_var, neighbors[0], 0])
                cnf.append([-edge_var, neighbors[1], 0])
        elif len(neighbors) > 2:
            clause_pairs = []
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    clause_pairs.append([-edge_to_var[edge], neighbors[i], neighbors[j], 0])
            cnf.extend(clause_pairs)
        else:
            # edge with less than two neighbors cannot be part of the cycle
            cnf.append([-edge_var, 0])

    # esures that each edge has at most two neighbors in the cycle
    if DEBUG : cnf.append("At most two neighbors")
    for edge in EDGES:
        neighbors = [ edge_to_var[neighbor] for neighbor in get_neighbors(edge)]
        if len(neighbors) > 2:
            for n in range(3, len(neighbors) + 1):
                for comb in combinations(neighbors, n):
                    clause = [-edge_to_var[edge]] + [ -var for var in comb]
                    cnf.append(clause + [0])

    # # ensure global connectivity
    # # if an edge is included in a cycle, ensure that the nodes connected by that edge are reachable
    # if DEBUG : cnf.append("Ensure global connectivity") # I didnt test this method
    # for edge in EDGES:
    #     edge_var = edge_to_var[edge]
    #     u, v = edge
    #     connected_edges_u = [edge_to_var[e] for e in EDGES if u in e and e != edge]
    #     connected_edges_v = [edge_to_var[e] for e in EDGES if v in e and e != edge]
    #     cnf.append([-edge_var] + connected_edges_u + [0])
    #     cnf.append([-edge_var] + connected_edges_v + [0])


    # conditions i should encode?
    # TODO: 1. closed cycle requirement
    # TODO: 2. for each vertex in a cycle, the degree must be exactly 2?

    return cnf, nr_vars

def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    # print CNF into formula.cnf in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    # call the solver and return the output
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity) , output_name], stdout=subprocess.PIPE)

def print_result(result):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)                 # print the whole output of the SAT solver to stdout, so you can see the raw output for yourself

    # check the returned result
    if (result.returncode == 20):   # returncode for SAT is 10, for UNSAT is 20
        return

    # parse the model from the output of the solver
    # the model starts with 'v'
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):    # there might be more lines of the model, each starting with 'v'
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)      
    model.remove(0) # 0 is the end of the model, just ignore it

    print()
    print("##################################################################")
    print("###########[ Human readable result of the tile puzzle ]###########")
    print("##################################################################")
    print()

    print(model)

    # TODO: print the edges in the cycle
    # TODO: print if this cycle is simple?

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # get the input instance
    instance = load_instance(args.input)

    # encode the problem to create CNF formula
    cnf, nr_vars = encode(instance)

    if DEBUG:
        print_cnf(cnf)
        exit()

    # call the SAT solver and get the result
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)

    # Interpret the result and print it in a human-readable format
    print_result(result)

# TODO: Finish print_result() method
# TODO: Add more input files
