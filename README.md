# Documentation

## Problem description

The Rural Postman problem involves finding a cycle in a graph that efficiently covers specific edges while adhering to certain limitations. Specifically, given an undirected graph with a set of nodes and edges, along with a subset F of required edges, the challenge is to determine if there exists a cycle that includes every edge in F, uses at most k edges in total, and allows nodes to be revisited (although, each edge can only occur once in the cycle). More information about the Rural Postman problem can be found [online](https://en.wikipedia.org/wiki/Chinese_postman_problem).

An example of a valid input format is:

```
4
4
0 1 1
0 2 0
1 2 0
1 3 0
2 3 1
```

where the first line is the number of vertices in th graph. Second line is k (maximum length of the cycle). The other lines represent the edges of the graph. The first two numbers of the lines are the indecies of the vertices that form the edge, the third number of the line is a value 1 or 0, True or False, which represents whether the edge is required (in a subset F).


I dont have it yet

```
I dont have it yet
```

## Encoding

I dont have it yet

## User documentation


Basic usage: 
```
rural_postman.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

## Example instances

I dont have it yet

## Experiments

I dont have it yet