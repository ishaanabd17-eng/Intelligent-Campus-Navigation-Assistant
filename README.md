<div align="center">

```
╔══════════════════════════════════════════════════════════╗
║    INTELLIGENT CAMPUS NAVIGATION ASSISTANT               ║
║    KL University · Hyderabad Campus                      ║
║    Algorithms: BFS  ·  UCS  ·  A*                        ║
╚══════════════════════════════════════════════════════════╝
```

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Search_Algorithms-00C896?style=for-the-badge)
![Course](https://img.shields.io/badge/Course-CFAI-6C63FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

**An AI-powered terminal navigation system that finds the optimal route between campus locations using BFS, UCS, and A\* Search.**

</div>

---

## 📌 Overview

The **Intelligent Campus Navigation Assistant** models KL University's Hyderabad campus as a **weighted graph** and applies AI search algorithms to compute the best route between any two locations.

```
Every location  →  a node  (state)
Every path      →  an edge (action)
Every edge has  →  distance cost + walking time
```

The system compares three algorithms side-by-side so you can see exactly how each one thinks differently.

---

## 🗺️ Campus Graph — 11 Locations

```
🚪 Main Gate ──────────────────────────────────────────
     │                                                  
     ├──▶ 🅿️  Parking       [ 6u  | 4min ]              
     ├──▶ 🏠  Hostel        [ 10u | 8min ]              
     ├──▶ 🍽️  Cafeteria     [ 8u  | 6min ]              
     ├──▶ 🌿  Central Plaza [ 5u  | 3min ]              
     └──▶ 🏢  Office        [ 4u  | 3min ]              
                                                        
🌿 Central Plaza ──────────────────────────────────────
     ├──▶ ⚽  Ground        [ 3u  | 2min ]              
     ├──▶ 🎭  Auditorium    [ 4u  | 3min ]              
     ├──▶ 📚  Library       [ 5u  | 4min ]              
     ├──▶ 🍽️  Cafeteria     [ 5u  | 4min ]              
     ├──▶ 🚪  Main Gate     [ 5u  | 3min ]              
     └──▶ 🏢  Office        [ 6u  | 4min ]              
                                                        
🍽️  Cafeteria ─────────────────────────────────────────
     ├──▶ 🌿  Central Plaza [ 5u  | 4min ]              
     ├──▶ 🎭  Auditorium    [ 4u  | 3min ]              
     ├──▶ 📚  Library       [ 4u  | 3min ]              
     ├──▶ 🔬  Lab           [ 3u  | 2min ]              
     ├──▶ 🏥  Medical Room  [ 2u  | 2min ]              
     └──▶ ⚽  Ground        [ 2u  | 1min ]              
```

| # | Icon | Location | Connections |
|---|------|----------|-------------|
| 01 | 🚪 | Main Gate | 5 |
| 02 | 🅿️ | Parking | 3 |
| 03 | 🏠 | Hostel | 2 |
| 04 | 🍽️ | Cafeteria | 6 |
| 05 | 🎭 | Auditorium | 4 |
| 06 | 📚 | Library | 4 |
| 07 | 🏢 | Office | 4 |
| 08 | 🏥 | Medical Room | 4 |
| 09 | 🔬 | Lab | 2 |
| 10 | ⚽ | Ground | 2 |
| 11 | 🌿 | Central Plaza | 6 |

---

## 🧠 AI Concepts Demonstrated

| Concept | Implementation |
|--------|----------------|
| **Problem Formulation** | Find optimal route between source and destination |
| **State-Space Representation** | Campus locations as graph nodes |
| **Cost Modelling** | Distance + walking time as edge weights |
| **Heuristic Search** | A\* uses admissible h(n) estimates per destination |
| **Graph Algorithms** | BFS, UCS, A\* on a weighted undirected graph |

---

## ⚙️ Algorithms

### 🔵 BFS — Breadth-First Search
> *"Fewest hops, regardless of cost"*

- Explores level by level using a **FIFO queue**
- Guarantees minimum number of hops
- Ignores edge weights completely
- `Time: O(V + E)` · `Space: O(V)`

---

### 🟢 UCS — Uniform Cost Search
> *"Cheapest path, always"*

- Uses a **Min-Heap priority queue**
- Always expands the node with lowest cumulative cost g(n)
- Guarantees optimal (minimum cost) path
- `Time: O((V + E) log V)` · `Space: O(V)`

---

### 🟠 A\* — A Star Search
> *"Smart, fast, and optimal"*

- Combines actual cost + heuristic estimate:

```
f(n) = g(n) + h(n)

  g(n) → actual cost from source to node n
  h(n) → estimated cost from n to goal
  f(n) → total estimated cost through n
```

- Explores **far fewer nodes** than UCS thanks to h(n)
- Optimal when heuristic is admissible (never overestimates)
- `Time: O((V + E) log V)` · `Space: O(V)`

---

## 📊 Algorithm Comparison — Main Gate → Library

```
╔══════════╦══════════╦══════════╦═══════╦════════════════╗
║ Algo     ║  Dist    ║  Time    ║ Hops  ║ Nodes Explored ║
╠══════════╬══════════╬══════════╬═══════╬════════════════╣
║ BFS      ║ 12u      ║ 9 min    ║ 2  ✓  ║ 4              ║
║ UCS      ║ 8u  ✓    ║ 6 min    ║ 2  ✓  ║ 9              ║
║ A*       ║ 8u  ✓    ║ 6 min    ║ 2  ✓  ║ 3  ✓           ║
╚══════════╩══════════╩══════════╩═══════╩════════════════╝
✓ = best in that category
```

**Paths taken:**
```
BFS  →  🚪 Main Gate  →  🍽️ Cafeteria  →  📚 Library       (dist: 12)
UCS  →  🚪 Main Gate  →  🏢 Office     →  📚 Library       (dist: 8)
A*   →  🚪 Main Gate  →  🏢 Office     →  📚 Library       (dist: 8, nodes: 3)
```

**Key insight:**
- BFS found a different (longer) route because it ignores edge costs
- UCS and A\* found the same optimal path, but A\* only explored **3 nodes vs 9** — that's the heuristic working

---

## 💻 Features

```
✅  Menu-driven terminal interface
✅  Color-coded output per algorithm (BFS=cyan, UCS=teal, A*=orange)
✅  Step-by-step route display with distance per hop
✅  Algorithm comparison table with ✓ best-in-category markers
✅  Paths taken section showing all 3 routes side by side
✅  Heuristics defined for 7 destination nodes
✅  11 campus locations with real layout connections
✅  Input validation with helpful error messages
✅  Campus graph adjacency list view
✅  Key insights printed after every comparison
```

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/faizaanmd2908-design/Intelligent-Campus-Navigation-Assistant

# Navigate into the folder
cd Intelligent-Campus-Navigation-Assistant

# Run the program
python main.py
```

> No external libraries needed — uses only Python standard library (`heapq`, `collections`)

---

## 🖥️ Sample Output

```
  ╔══════════════════════════════════════════════════════════╗
  ║    INTELLIGENT CAMPUS NAVIGATION SYSTEM                  ║
  ║    KL University · Hyderabad Campus                      ║
  ║    Algorithms: BFS  ·  UCS  ·  A*                        ║
  ╚══════════════════════════════════════════════════════════╝

  [1]  🔍  Find Optimal Route
  [2]  📋  View Campus Locations
  [3]  🗺️  View Campus Graph Map
  [4]  ⚡  Compare All Algorithms
  [5]  👋  Exit

  ❯ Enter option (1–5):
```

```
  A* — A* Heuristic Search

   START  🚪  Main Gate
          │  4u · 3min
          ▼
    [1]   🏢  Office
          │  4u · 3min
          ▼
    END   📚  Library

  📏  Distance        →  8 units
  ⏱️   Time           →  6 min
  🔗  Hops            →  2
  🔎  Nodes Explored  →  3

  ✔  Path found successfully
```

---

## 🌍 Real-World Applications

- 🗺️ Google Maps & GPS routing
- 🤖 Robot path planning
- 🎮 Game AI navigation
- 🚗 Autonomous vehicle routing
- 📦 Delivery route optimization
- 🏫 Smart campus systems

---

## 🔮 Future Enhancements

- [ ] GUI-based interactive campus map with visual pathfinding
- [ ] Real-time congestion and obstacle handling
- [ ] GPS integration with live location
- [ ] Mobile application version
- [ ] Dynamic heuristic generation using ML
- [ ] Voice-enabled navigation
- [ ] Web interface using Flask

---

## 👨‍💻 Team

| Name | Roll Number |
|------|-------------|
| Faizaan | 2520030359 |
| Ishaan | 2520030267 |
| Anirudh | 2520080058 |

**Course:** Computational Foundations of Artificial Intelligence (CFAI)
**Institution:** KL University, Hyderabad — Bachupally Campus

---

## 📝 Conclusion

This project demonstrates how AI search algorithms solve real-world navigation problems. The side-by-side comparison of BFS, UCS, and A\* makes it clear how uninformed, cost-based, and heuristic-guided search differ in both path quality and efficiency.

---

<div align="center">
<sub>Built with Python · CFAI Mini Project · KL University Hyderabad</sub>
</div>