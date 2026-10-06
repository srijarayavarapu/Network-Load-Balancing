## Job Migration Minimization using Breadth-First Search (BFS)

This project focuses on efficiently managing jobs across a capacity-limited network of computer servers. When a job is assigned to a server that has reached its maximum capacity, the system searches for the nearest server with available space and moves the job through the shortest possible route. The project uses the **Breadth-First Search (BFS)** algorithm to minimize the number of migrations required.

## Problem Description

The network consists of multiple interconnected computer systems represented as nodes in a graph. Each node has a maximum capacity that determines how many jobs it can handle at a time.

- **Nodes:** Represent individual servers in the network.
- **Node Capacity:** Defines the maximum number of jobs that a server can accommodate.
- **Edges:** Represent direct connections between two servers.
- **Migration:** Represents moving a job from one server to a connected server.

When a job is submitted to a server with available capacity, it is processed directly. However, if the selected server is already full, the job must be moved to another connected server. The objective is to find an available server using the minimum possible number of migrations.

### Example Scenario

Assume that server `N2` has a maximum capacity of `4` and is currently running four jobs: `J5`, `J6`, `J7`, and `J8`.

If a new job `J14` is submitted to `N2`, the server cannot accept it because it is already full. The system therefore searches connected servers such as `N1` and `N4` to identify the nearest server with available capacity.

## Algorithm: Breadth-First Search (BFS)

**Breadth-First Search (BFS)** is used to identify the closest available server in the network. Since the network is treated as an unweighted graph, BFS explores nodes according to their distance from the starting server. Each edge represents one possible job migration, so the shortest path corresponds to the minimum number of migrations.

The process works as follows:

**Job Submission:**  
A new job is submitted to a particular server in the network.

**Capacity Verification:**  
The system first checks whether the selected server has free capacity.

- If capacity is available, the job is assigned directly.
- The number of migrations is `0`.

If the server is full, the system begins searching for another suitable server.

**Start BFS:**  
BFS begins from the overloaded server and explores its connected neighbors.

A queue is used to manage the servers waiting to be explored, while a visited set prevents the same server from being processed multiple times.

**Level-by-Level Exploration:**  
BFS searches the network in levels:

- First, it examines directly connected servers — `1 migration`.
- If none of them has available capacity, it examines the next level — `2 migrations`.
- The search continues until a server with free capacity is found.

**Select Destination:**  
The first available server reached by BFS provides the shortest migration path from the original server. The number of edges in this path represents the minimum number of migrations required.

**No Available Server:**  
If BFS explores all reachable servers and none has available capacity, the job cannot be assigned within the reachable portion of the network.

### BFS Process

Start at overloaded server
          ↓
Check available capacity
          ↓
   Is capacity available?
       ↙          ↘
     Yes           No
      ↓             ↓
 Assign Job     Start BFS
      ↓             ↓
    Finish      Explore neighbors
                    ↓
             Is capacity available?
                ↙          ↘
              Yes           No
               ↓             ↓
          Assign Job    Continue BFS
               ↓             ↓
             Finish    Explore next level
                              ↓
                         Repeat search



<img width="597" height="934" alt="Job migration output" src="https://github.com/user-attachments/assets/028f246e-b0a6-45fa-a368-62ad78b551fe" />
