#!/bin/bash

TIME_LOG="execution_times.log"
echo -e "N\tK\tTime (s)" > $TIME_LOG

# highest boundaries for N and K
MAX_N=$1
MAX_K=$2

# check if both arguments are provided
if [ -z "$MAX_N" ] || [ -z "$MAX_K" ]; then
    echo "Usage: $0 <MAX_N> <MAX_K>"
    exit 1
fi

# iterate over all combinations of N and K
for ((N=1; N<=MAX_N; N++)); do
    for ((K=1; K<=MAX_K; K++)); do
        echo "Running experiment for N=$N, K=$K..."
        
        # generate the graph using graph_generator.py
        python3 graph_generator.py -n "$N" -k "$K" -o "generated_graph.in"

        # measure execution time of rural_postman.py
        START_TIME=$(date +%s.%N)
        python3 rural_postman.py -i "generated_graph.in" -o "formula.cnf" -s "glucose-syrup" -v 1
        END_TIME=$(date +%s.%N)

        # calculate elapsed time
        ELAPSED_TIME=$(echo "$END_TIME - $START_TIME" | bc)

        # log N, K, and elapsed time to the file
        echo -e "$N\t$K\t$ELAPSED_TIME" >> $TIME_LOG

        echo "Experiment for N=$N, K=$K completed. Time: $ELAPSED_TIME seconds."
    done
done

echo "All experiments completed. Results logged in $TIME_LOG."
