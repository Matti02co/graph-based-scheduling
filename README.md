# Scheduling to Graph Transformation

This repository contains two academic projects focused on solving a specific process scheduling problem and exploring alternative approaches by modeling it as a graph problem.

## Problem Description

We consider a scheduling scenario with:

- A single processor with a fixed number of cores,
  
- A time limit for process execution.
  
A set of processes, each with:

- execution time,
  
- associated profit.

The goal is to maximize the total profit by selecting processes to schedule on the available cores without exceeding the time limit.
This makes the problem similar to a Knapsack problem.

## Project Structure

### Part 1 – Scheduling & Knapsack Formulation

- Formulation of the problem as a Knapsack-like optimization problem.

- Solution using IBM CPLEX.

- Comparison with classic scheduling algorithms such as:

 - Shortest Process First (SPF)

 - First Come First Served (FCFS)

This part is documented in the first report.

### Part 2 – Graph Transformation

Reformulation of the same scheduling problem as a graph problem.

Explanation of:

- Why the transformation is possible.

- How the problem constraints and objectives are represented in the graph.

Solution approaches:

- Using CPLEX on the graph formulation.

- Applying shortest/longest path algorithms directly.

This part is documented in the second report.

## Repository Contents

- `docs/` → Project reports (PDFs).

- `code/` → Source code for both parts.

## Future Improvements

I am currently working on this repo, in the next few weeks I will provide:

- Clean, modular Python implementation of the algorithms.

- Examples and benchmarks.

- English translation of reports.
