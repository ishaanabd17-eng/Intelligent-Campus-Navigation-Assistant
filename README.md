# 🎓 Intelligent Campus Navigation Assistant

> **Course:** Computational Foundations of Artificial Intelligence (CFAI)
> **Programming Language:** Python

---

# 📌 Project Overview

The **Intelligent Campus Navigation Assistant** is an Artificial Intelligence-based mini project that models a college campus as a **weighted graph** and applies AI search algorithms to determine the optimal route between campus locations.

In this project:

* Each campus location is represented as a **node/state**
* Each connecting path is represented as an **edge/action**
* Every edge contains:

  * Distance Cost
  * Estimated Walking Time

The system intelligently computes the best path using:

* Breadth-First Search (BFS)
* Uniform Cost Search (UCS)
* A* Search Algorithm

---

# 🧠 AI Concepts Demonstrated

| AI Concept                 | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| Problem Formulation        | Finding the optimal path between source and destination |
| State-Space Representation | Campus locations represented as graph nodes             |
| Cost Modeling              | Distance and time used as path costs                    |
| Heuristic Search           | A* uses heuristic estimates h(n)                        |
| Graph Search Algorithms    | BFS, UCS, and A* traversal                              |

---

# 🗺️ Campus Locations (Nodes)

The campus graph contains the following locations:

1. Main Gate
2. Parking
3. Hostel
4. Cafeteria
5. Auditorium
6. Library
7. Office
8. Medical Room
9. Lab

---

# 🔗 Campus Graph Connections

| From         | To           | Distance | Time  |
| ------------ | ------------ | -------- | ----- |
| Main Gate    | Parking      | 4 units  | 3 min |
| Main Gate    | Hostel       | 8 units  | 6 min |
| Main Gate    | Office       | 5 units  | 4 min |
| Main Gate    | Cafeteria    | 6 units  | 5 min |
| Parking      | Cafeteria    | 5 units  | 4 min |
| Parking      | Hostel       | 7 units  | 5 min |
| Cafeteria    | Auditorium   | 3 units  | 2 min |
| Cafeteria    | Library      | 4 units  | 3 min |
| Cafeteria    | Medical Room | 2 units  | 2 min |
| Auditorium   | Library      | 2 units  | 2 min |
| Auditorium   | Office       | 3 units  | 2 min |
| Auditorium   | Medical Room | 2 units  | 1 min |
| Library      | Office       | 4 units  | 3 min |
| Library      | Medical Room | 2 units  | 2 min |
| Medical Room | Lab          | 3 units  | 2 min |
| Lab          | Office       | 2 units  | 1 min |

---

# ⚙️ Algorithms Implemented

## 1️⃣ Breadth-First Search (BFS)

### Description

* Explores nodes level by level using a FIFO queue
* Finds the path with minimum number of hops
* Does not consider edge weights

### Complexity

* **Time Complexity:** O(V + E)
* **Space Complexity:** O(V)

### Use Case

Useful when all edges have equal cost.

---

## 2️⃣ Uniform Cost Search (UCS)

### Description

* Uses a priority queue (Min Heap)
* Expands the node with minimum cumulative cost
* Guarantees the optimal shortest path

### Complexity

* **Time Complexity:** O((V + E) log V)
* **Space Complexity:** O(V)

### Use Case

Best for weighted graphs where path cost matters.

---

## 3️⃣ A* Search Algorithm

### Description

A* uses the formula:

f(n) = g(n) + h(n)

Where:

* g(n) → Actual cost from source
* h(n) → Estimated cost to goal (heuristic)
* f(n) → Total estimated path cost

### Features

* Faster than UCS due to heuristic guidance
* Explores fewer nodes
* Produces optimal paths with admissible heuristics

### Complexity

* **Time Complexity:** O((V + E) log V)
* **Space Complexity:** O(V)

---

# 📊 Heuristic Function

The project uses heuristic values for intelligent path estimation in A* Search.

The heuristic function:

* Estimates the remaining distance to the destination
* Helps A* prioritize better paths
* Never overestimates actual cost (Admissible Heuristic)

This guarantees optimal results.

---

# 🖥️ Features of the Project

✅ Menu-driven terminal interface
✅ Professional colored terminal output
✅ BFS, UCS, and A* implementation
✅ Graph representation using adjacency list
✅ Route distance and time calculation
✅ Algorithm comparison table
✅ Input validation and error handling
✅ Campus graph visualization
✅ Detailed comments for learning and understanding

---

# 📸 Project Outputs Included

The project includes:

* Campus graph image
* Main menu screenshot
* Route finding output screenshot
* Algorithm comparison screenshot
* Campus locations screenshot
* Campus graph adjacency list screenshot

---

# 🚀 How to Run the Project

## Step 1: Open Terminal

Navigate to the project folder.

## Step 2: Run the Program

```bash
python campus_navigation.py
```

---

# 📌 Sample Output

```text
Algorithm Used : A*

Optimal Route:
Parking → Cafeteria → Medical Room → Lab

Total Distance : 10 units
Estimated Time : 8 minutes
Total Hops     : 3
Nodes Explored : 4

✔ SUCCESS — Path Found
```

---

# 📈 Algorithm Comparison Example

| Algorithm | Distance | Time  | Hops | Nodes Explored |
| --------- | -------- | ----- | ---- | -------------- |
| BFS       | 11       | 9 min | 3    | 7              |
| UCS       | 10       | 8 min | 3    | 6              |
| A*        | 10       | 8 min | 3    | 4              |

### Observation

* BFS minimizes hops
* UCS minimizes total path cost
* A* finds optimal paths more efficiently using heuristics

---

# 🌍 Real World Applications

* Google Maps Navigation
* GPS Routing Systems
* Robot Path Planning
* Smart Campus Navigation
* Delivery Route Optimization
* Game AI Navigation Systems
* Autonomous Vehicle Navigation

---

# 🔮 Future Enhancements

* GUI-based interactive campus map
* Real-time congestion handling
* GPS integration
* Voice-enabled navigation
* Mobile application version
* Dynamic heuristic generation
* Machine Learning-based travel prediction

---

# 📝 Conclusion

This project successfully demonstrates how Artificial Intelligence search algorithms can solve real-world navigation problems efficiently.

The implementation of BFS, UCS, and A* provides a clear understanding of:

* uninformed search,
* cost-based search,
* and heuristic-guided intelligent search techniques.

The project is educational, beginner-friendly, and showcases practical applications of AI in navigation systems.

---

# 👨‍💻 Project Team

This project was developed as a team project for the CFAI course.

## Team Members

* Faizaan (2520030359)
* Ishaan (2520030267)
* Anirudh (2520080058)

## Course

Computational Foundations of Artificial Intelligence (CFAI)

## Project Title

Intelligent Campus Navigation Assistant using BFS, UCS, and A* Search Algorithms
