"""
=============================================================================
        INTELLIGENT CAMPUS NAVIGATION ASSISTANT
        CFAI (Computational Foundations of Artificial Intelligence)
        Mini Project

  AI Concepts Demonstrated:
  ─────────────────────────────────────────────────
  1. Problem Formulation
     → Find the shortest/optimal route between two campus locations.

  2. State-Space Representation
     → Each campus location is a STATE (node).
     → Moving from one location to another is an ACTION (edge).
     → The GOAL is to reach the destination from the source.

  3. Cost Modeling
     → Every path between locations has a COST (distance + time).
     → We try to minimize this cost to find the OPTIMAL path.

  4. Heuristic Search
     → A* uses a heuristic h(n) to ESTIMATE cost to the goal.
     → This makes the search smarter and faster.

  5. Graph Search Algorithms
     → BFS  : Explores level by level (minimizes hops)
     → UCS  : Explores by minimum cumulative cost (optimal)
     → A*   : Uses f(n) = g(n) + h(n) (optimal + intelligent)

  Standard Library Used:
  → heapq            : Priority queue for UCS and A*
  → collections.deque: Queue for BFS

=============================================================================
"""

# ── Standard library imports (no external packages needed) ─────────────────
import heapq                   # Min-heap / Priority Queue
from collections import deque  # Double-ended queue (for BFS)

# ══════════════════════════════════════════════════════════════════════════
#  SECTION 1 ─ ANSI COLOR CODES
#  These make the terminal output look professional and colorful.
#  How it works: wrapping text in escape codes changes its display color.
# ══════════════════════════════════════════════════════════════════════════

class C:
    """
    ANSI escape codes for terminal colors.
    Usage: print(C.GREEN + "text" + C.RESET)
    """
    RESET    = '\033[0m'
    BOLD     = '\033[1m'
    RED      = '\033[91m'
    GREEN    = '\033[92m'
    YELLOW   = '\033[93m'
    BLUE     = '\033[94m'
    MAGENTA  = '\033[95m'
    CYAN     = '\033[96m'
    WHITE    = '\033[97m'
    DIM      = '\033[2m'


def colorize(color_code, text):
    """Wrap text in color code and reset. Shortcut for coloring output."""
    return f"{color_code}{text}{C.RESET}"


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 2 ─ CAMPUS GRAPH (STATE-SPACE REPRESENTATION)
#
#  Each key in the dictionary = a campus LOCATION (node/state)
#  Each value = list of (neighbor, distance, walking_time)
#
#  This is an ADJACENCY LIST — the standard way to represent a graph
#  in code because:
#    - Memory efficient (stores only existing edges)
#    - Easy to traverse neighbors
#    - Suitable for BFS, UCS, and A*
#
#  Graph is UNDIRECTED: if A→B exists, B→A also exists.
#  Graph is WEIGHTED  : each edge has a numerical cost (distance).
# ══════════════════════════════════════════════════════════════════════════

CAMPUS_GRAPH = {

    # ── Entry Point ─────────────────────────────────────────────────────
    "Main Gate": [
        ("Parking",   4, 3),   # 4 units away, 3 min walk
        ("Hostel",    8, 6),   # 8 units away, 6 min walk
        ("Office",    5, 4),   # 5 units away, 4 min walk
        ("Cafeteria", 6, 5),   # 6 units away, 5 min walk
    ],

    # ── Parking Area ─────────────────────────────────────────────────────
    "Parking": [
        ("Main Gate",  4, 3),
        ("Cafeteria",  5, 4),
        ("Hostel",     7, 5),
    ],

    # ── Hostel (Residential) ──────────────────────────────────────────────
    "Hostel": [
        ("Main Gate",  8, 6),
        ("Parking",    7, 5),
    ],

    # ── Cafeteria (Central Hub) ────────────────────────────────────────────
    "Cafeteria": [
        ("Main Gate",    6, 5),
        ("Parking",      5, 4),
        ("Auditorium",   3, 2),
        ("Library",      4, 3),
        ("Medical Room", 2, 2),
    ],

    # ── Auditorium ────────────────────────────────────────────────────────
    "Auditorium": [
        ("Cafeteria",    3, 2),
        ("Library",      2, 2),
        ("Office",       3, 2),
        ("Medical Room", 2, 1),
    ],

    # ── Library ───────────────────────────────────────────────────────────
    "Library": [
        ("Cafeteria",    4, 3),
        ("Auditorium",   2, 2),
        ("Office",       4, 3),
        ("Medical Room", 2, 2),
    ],

    # ── Office (Administration) ────────────────────────────────────────────
    "Office": [
        ("Main Gate",  5, 4),
        ("Auditorium", 3, 2),
        ("Library",    4, 3),
        ("Lab",        2, 1),
    ],

    # ── Medical Room ──────────────────────────────────────────────────────
    "Medical Room": [
        ("Cafeteria",  2, 2),
        ("Auditorium", 2, 1),
        ("Library",    2, 2),
        ("Lab",        3, 2),
    ],

    # ── Laboratory ────────────────────────────────────────────────────────
    "Lab": [
        ("Medical Room", 3, 2),
        ("Office",       2, 1),
    ],
}


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 3 ─ HEURISTIC TABLE FOR A* SEARCH
#
#  What is a Heuristic?
#  → h(n) is an ESTIMATED cost from node n to the GOAL.
#  → It guides A* toward the goal without exploring every node.
#
#  Admissible Heuristic:
#  → A heuristic is ADMISSIBLE if it NEVER OVERESTIMATES the true cost.
#  → This guarantees A* finds the OPTIMAL (shortest) path.
#
#  A* Formula:
#  → f(n) = g(n) + h(n)
#     • g(n) = actual cost from START to node n (known exactly)
#     • h(n) = estimated cost from node n to GOAL (heuristic guess)
#     • f(n) = total estimated cost through node n
#
#  A* always expands the node with the LOWEST f(n) first.
#  This is smarter than UCS (which ignores h) and BFS (which ignores cost).
# ══════════════════════════════════════════════════════════════════════════

HEURISTICS = {
    # Heuristic values when HOSTEL is the goal node
    "Hostel": {
        "Hostel":       0,   # Already at goal → h = 0
        "Main Gate":    7,   # Estimated 7 units from Main Gate to Hostel
        "Parking":      6,   # Parking is close to Hostel via Main Gate
        "Office":       8,
        "Cafeteria":    9,
        "Auditorium":   7,
        "Library":      8,
        "Medical Room": 6,
        "Lab":          7,
    }
}


def get_heuristic(node, goal):
    """
    Returns h(n): estimated cost from 'node' to 'goal'.
    If goal has no heuristic table → returns 0 (acts like UCS).
    h(n) = 0 is always admissible (never overestimates).
    """
    if goal in HEURISTICS and node in HEURISTICS[goal]:
        return HEURISTICS[goal][node]
    return 0  # Default: no heuristic (admissible fallback)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 4 ─ RESULT DATA STRUCTURE
#  Stores all output from a completed search.
# ══════════════════════════════════════════════════════════════════════════

class SearchResult:
    """
    Holds everything we want to display after a search.
    Attributes:
        path           : List of location names from source to destination
        total_distance : Sum of edge distances along the path
        total_time     : Sum of edge times along the path
        nodes_explored : How many nodes the algorithm visited
        algorithm      : Name of algorithm used (BFS / UCS / A*)
        found          : True if a path was found, False otherwise
    """
    def __init__(self, path, total_distance, total_time,
                 nodes_explored, algorithm, found=True):
        self.path           = path
        self.total_distance = total_distance
        self.total_time     = total_time
        self.nodes_explored = nodes_explored
        self.algorithm      = algorithm
        self.found          = found


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 5 ─ UTILITY: CALCULATE PATH COST
#  Given a list of node names (path), compute total distance and time.
# ══════════════════════════════════════════════════════════════════════════

def calculate_path_cost(path):
    """
    Walk through each consecutive pair in the path.
    Look up the edge in the graph and sum distance + time.

    Example: ["Main Gate", "Parking", "Hostel"]
    → Main Gate→Parking: dist=4, time=3
    → Parking→Hostel   : dist=7, time=5
    → Total: dist=11,  time=8
    """
    total_distance = 0
    total_time     = 0

    for i in range(len(path) - 1):
        source      = path[i]
        destination = path[i + 1]

        # Find matching edge in adjacency list
        for (neighbor, dist, t) in CAMPUS_GRAPH.get(source, []):
            if neighbor == destination:
                total_distance += dist
                total_time     += t
                break

    return total_distance, total_time


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 6 ─ ALGORITHM 1: BFS (BREADTH-FIRST SEARCH)
#
#  How BFS works:
#  ─────────────────────────────────────────────────────
#  1. Start from the source node.
#  2. Explore ALL neighbors at distance 1 (level 1).
#  3. Then ALL neighbors at distance 2 (level 2).
#  4. Continue until goal is found.
#
#  Uses a FIFO QUEUE (deque) → First In, First Out.
#  Guarantees: Minimum number of HOPS (edges traversed).
#  Does NOT guarantee: minimum COST (ignores edge weights).
#
#  Time Complexity : O(V + E)  where V=nodes, E=edges
#  Space Complexity: O(V)
# ══════════════════════════════════════════════════════════════════════════

def bfs(source, destination):
    """
    Breadth-First Search from source to destination.

    State: (current_node, path_taken_so_far)
    Queue: deque → FIFO order (level-by-level exploration)
    Visited set: prevents revisiting nodes (avoid cycles)

    Returns: SearchResult object
    """

    # Edge case: source IS the destination
    if source == destination:
        return SearchResult([source], 0, 0, 1, "BFS")

    # Initialize FIFO queue with starting state
    # Each item: (current_location, path_from_source)
    queue   = deque([(source, [source])])
    visited = set([source])   # Track visited nodes
    nodes_explored = 0        # Counter for performance measurement

    while queue:
        # Dequeue the FIRST item (FIFO = level-order)
        current_node, current_path = queue.popleft()
        nodes_explored += 1

        # Explore each neighbor of current node
        for (neighbor, distance, time) in CAMPUS_GRAPH.get(current_node, []):

            if neighbor not in visited:
                new_path = current_path + [neighbor]

                # GOAL TEST: have we reached the destination?
                if neighbor == destination:
                    dist, t = calculate_path_cost(new_path)
                    return SearchResult(
                        path           = new_path,
                        total_distance = dist,
                        total_time     = t,
                        nodes_explored = nodes_explored + 1,
                        algorithm      = "BFS"
                    )

                # Not goal yet: mark visited and add to queue
                visited.add(neighbor)
                queue.append((neighbor, new_path))

    # Queue emptied without finding goal → no path exists
    return SearchResult([], 0, 0, nodes_explored, "BFS", found=False)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 7 ─ ALGORITHM 2: UCS (UNIFORM COST SEARCH)
#
#  How UCS works:
#  ─────────────────────────────────────────────────────
#  1. Always expand the node with the LOWEST cumulative cost g(n).
#  2. Uses a MIN-HEAP (priority queue) ordered by g(n).
#  3. Guarantees OPTIMAL path (minimum total cost/distance).
#
#  Difference from BFS:
#  → BFS ignores edge weights (counts hops).
#  → UCS respects edge weights (minimizes total cost).
#
#  Time Complexity : O((V + E) log V)
#  Space Complexity: O(V)
# ══════════════════════════════════════════════════════════════════════════

def ucs(source, destination):
    """
    Uniform Cost Search from source to destination.

    Priority Queue item: (cumulative_cost, current_node, path)
    → heapq is a MIN-HEAP: always pops the SMALLEST cost item first.

    Returns: SearchResult object
    """

    if source == destination:
        return SearchResult([source], 0, 0, 1, "UCS")

    # Priority queue: (g_cost, node, path)
    # g_cost = total cost accumulated from source to this node
    priority_queue = [(0, source, [source])]
    visited        = {}    # node → best cost seen so far
    nodes_explored = 0

    while priority_queue:
        # Pop node with MINIMUM cumulative cost
        g_cost, current_node, current_path = heapq.heappop(priority_queue)
        nodes_explored += 1

        # Skip if we already found a cheaper path to this node
        if current_node in visited and visited[current_node] <= g_cost:
            continue

        # Record the best cost to reach this node
        visited[current_node] = g_cost

        # GOAL TEST
        if current_node == destination:
            dist, t = calculate_path_cost(current_path)
            return SearchResult(
                path           = current_path,
                total_distance = dist,
                total_time     = t,
                nodes_explored = nodes_explored,
                algorithm      = "UCS"
            )

        # Expand neighbors
        for (neighbor, distance, time) in CAMPUS_GRAPH.get(current_node, []):
            new_cost = g_cost + distance   # accumulate cost

            # Only push if cheaper path found
            if neighbor not in visited or visited[neighbor] > new_cost:
                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor, current_path + [neighbor])
                )

    return SearchResult([], 0, 0, nodes_explored, "UCS", found=False)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 8 ─ ALGORITHM 3: A* SEARCH
#
#  How A* works:
#  ─────────────────────────────────────────────────────
#  1. Like UCS, but adds a HEURISTIC h(n) to guide the search.
#  2. Uses: f(n) = g(n) + h(n)
#       • g(n) = actual cost from source to n (exact, known)
#       • h(n) = estimated cost from n to goal (heuristic)
#       • f(n) = total estimated solution cost through n
#  3. Always expands the node with lowest f(n).
#
#  Why A* is better than UCS:
#  → UCS explores equally in all directions (like ripples in a pond).
#  → A* is guided toward the GOAL by the heuristic.
#  → Result: fewer nodes explored, faster search.
#
#  Optimality condition:
#  → A* is OPTIMAL if h(n) is ADMISSIBLE (never overestimates).
#
#  Time Complexity : O((V + E) log V) — depends on heuristic quality
#  Space Complexity: O(V)
# ══════════════════════════════════════════════════════════════════════════

def astar(source, destination):
    """
    A* Search from source to destination.

    Priority Queue item: (f_cost, g_cost, current_node, path)
    f(n) = g(n) + h(n)

    Returns: SearchResult object
    """

    if source == destination:
        return SearchResult([source], 0, 0, 1, "A*")

    # Compute initial heuristic for source node
    h_start = get_heuristic(source, destination)

    # Priority queue: (f_cost, g_cost, node, path)
    priority_queue = [(h_start, 0, source, [source])]
    visited        = {}
    nodes_explored = 0

    while priority_queue:
        # Pop node with MINIMUM f(n) = g(n) + h(n)
        f_cost, g_cost, current_node, current_path = heapq.heappop(priority_queue)
        nodes_explored += 1

        # Skip already optimally resolved nodes
        if current_node in visited and visited[current_node] <= g_cost:
            continue
        visited[current_node] = g_cost

        # GOAL TEST
        if current_node == destination:
            dist, t = calculate_path_cost(current_path)
            return SearchResult(
                path           = current_path,
                total_distance = dist,
                total_time     = t,
                nodes_explored = nodes_explored,
                algorithm      = "A*"
            )

        # Expand neighbors using f(n) = g(n) + h(n)
        for (neighbor, distance, time) in CAMPUS_GRAPH.get(current_node, []):
            new_g = g_cost + distance             # actual cost to neighbor
            new_h = get_heuristic(neighbor, destination)  # estimated remaining
            new_f = new_g + new_h                 # total estimated cost

            if neighbor not in visited or visited[neighbor] > new_g:
                heapq.heappush(
                    priority_queue,
                    (new_f, new_g, neighbor, current_path + [neighbor])
                )

    return SearchResult([], 0, 0, nodes_explored, "A*", found=False)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 9 ─ DISPLAY FUNCTIONS
#  Professional terminal output using box-drawing characters + colors.
# ══════════════════════════════════════════════════════════════════════════

def print_banner():
    """Display the startup banner with project title."""
    banner = f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║                                                      ║
  ║      INTELLIGENT CAMPUS NAVIGATION SYSTEM            ║
  ║                                                      ║
  ║      AI Algorithms : BFS  |  UCS  |  A*              ║
  ║                                                      ║
  ║      CFAI Project                                    ║
  ║                                                      ║
  ╚══════════════════════════════════════════════════════╝
{C.RESET}"""
    print(banner)


def print_separator(char="─", width=56, color=C.DIM):
    """Print a horizontal separator line."""
    print(colorize(color, f"  {char * width}"))


def print_section_header(title, color=C.CYAN):
    """Print a styled section header."""
    print()
    print(colorize(color + C.BOLD, f"  ══  {title}  ══"))
    print()


def display_main_menu():
    """Display the main navigation menu."""
    print_section_header("MAIN MENU", C.YELLOW)
    options = [
        ("1", "Find Optimal Route"),
        ("2", "View Campus Locations"),
        ("3", "View Campus Graph Map"),
        ("4", "Compare All Algorithms"),
        ("5", "Exit"),
    ]
    for num, label in options:
        print(f"   {colorize(C.YELLOW + C.BOLD, num + '.')}  {label}")
    print()


def display_locations():
    """Display all available campus locations in a formatted list."""
    print_section_header("CAMPUS LOCATIONS", C.BLUE)
    all_locations = list(CAMPUS_GRAPH.keys())
    for i, loc in enumerate(all_locations, start=1):
        marker = colorize(C.GREEN + C.BOLD, f"  [{i:02}]")
        print(f"{marker}  {loc}")
    print()
    print(colorize(C.DIM, f"  Total locations: {len(all_locations)}"))
    print()


def display_campus_graph():
    """Display the adjacency list in a readable table format."""
    print_section_header("CAMPUS GRAPH — ADJACENCY LIST", C.BLUE)
    print(colorize(C.DIM, "  Format: Location → Neighbor (Distance units | Time min)"))
    print()

    for node, edges in CAMPUS_GRAPH.items():
        print(colorize(C.CYAN + C.BOLD, f"  📍 {node}"))
        for (neighbor, dist, time) in edges:
            arrow = colorize(C.DIM, "     └──▶")
            info  = colorize(C.GREEN, f"{neighbor}")
            cost  = colorize(C.YELLOW, f"({dist}u | {time}min)")
            print(f"{arrow}  {info}  {cost}")
        print()


def display_algorithm_menu():
    """Display algorithm selection sub-menu."""
    print()
    print(colorize(C.MAGENTA + C.BOLD, "  Select Algorithm:"))
    print()
    choices = [
        ("1", "BFS",  "Breadth-First Search — minimizes hops"),
        ("2", "UCS",  "Uniform Cost Search  — optimal by distance"),
        ("3", "A*",   "A* Search            — heuristic-guided optimal"),
    ]
    for num, algo, desc in choices:
        print(f"   {colorize(C.YELLOW + C.BOLD, num + '.')}  "
              f"{colorize(C.CYAN, algo):18}  {colorize(C.DIM, desc)}")
    print()


def display_result(result, source, destination):
    """
    Display the result of a single algorithm search.
    Shows path, distance, time, hops, nodes explored.
    """
    print()
    print_separator("═", 56, C.CYAN)
    print(colorize(C.CYAN + C.BOLD,
          f"  Algorithm Used : {result.algorithm}"))
    print_separator("═", 56, C.CYAN)
    print()

    if not result.found or not result.path:
        print(colorize(C.RED, "  ✗  No path found between the given locations."))
        print()
        return

    # Build route string with arrows
    route_str = colorize(C.GREEN + C.BOLD,
                         "  →  ".join(result.path))

    print(colorize(C.WHITE + C.BOLD, "  Optimal Route:"))
    print(f"  {route_str}")
    print()
    print_separator()

    # Stats table
    hops = len(result.path) - 1
    rows = [
        ("Total Distance", f"{result.total_distance} units"),
        ("Estimated Time", f"{result.total_time} minutes"),
        ("Total Hops",     f"{hops}"),
        ("Nodes Explored", f"{result.nodes_explored}"),
    ]
    for label, value in rows:
        lbl = colorize(C.DIM,    f"  {label:<18}:")
        val = colorize(C.YELLOW, f"  {value}")
        print(f"{lbl}{val}")

    print_separator()
    status = colorize(C.GREEN + C.BOLD, "  ✔  SUCCESS — Path Found")
    print(status)
    print()


def display_comparison(source, destination):
    """
    Run all three algorithms and display a comparison table.
    Makes it easy to see how algorithms differ in performance.
    """
    print_section_header(f"ALGORITHM COMPARISON  |  {source}  →  {destination}",
                         C.MAGENTA)

    # Run all three
    algorithms = [
        bfs(source, destination),
        ucs(source, destination),
        astar(source, destination),
    ]

    # ── Table header ─────────────────────────────────────────────────────
    header_color = C.MAGENTA + C.BOLD
    print(colorize(header_color,
        "  ╔════════════════╦══════════╦══════════╦══════════╦════════════════╗"))
    print(colorize(header_color,
        "  ║   Algorithm    ║ Distance ║ Time(min)║   Hops   ║ Nodes Explored ║"))
    print(colorize(header_color,
        "  ╠════════════════╬══════════╬══════════╬══════════╬════════════════╣"))

    # ── Table rows ────────────────────────────────────────────────────────
    for r in algorithms:
        if r.found and r.path:
            hops = len(r.path) - 1
            algo_col = f"{r.algorithm:<14}"
            dist_col = f"{r.total_distance:<8}"
            time_col = f"{r.total_time:<8}"
            hops_col = f"{hops:<8}"
            expl_col = f"{r.nodes_explored:<14}"
        else:
            algo_col = f"{r.algorithm:<14}"
            dist_col = f"{'N/A':<8}"
            time_col = f"{'N/A':<8}"
            hops_col = f"{'N/A':<8}"
            expl_col = f"{'N/A':<14}"

        row = (f"  ║ {colorize(C.CYAN, algo_col)} ║ "
               f"{colorize(C.YELLOW, dist_col)} ║ "
               f"{colorize(C.YELLOW, time_col)} ║ "
               f"{colorize(C.GREEN, hops_col)} ║ "
               f"{colorize(C.GREEN, expl_col)} ║")
        print(row)

    print(colorize(header_color,
        "  ╚════════════════╩══════════╩══════════╩══════════╩════════════════╝"))
    print()

    # ── Insight note ──────────────────────────────────────────────────────
    print(colorize(C.DIM,
        "  💡 A* typically explores fewer nodes than BFS and UCS,"))
    print(colorize(C.DIM,
        "     thanks to its heuristic function h(n) guiding the search."))
    print()

    # Also display individual full results
    print_section_header("DETAILED RESULTS", C.CYAN)
    for r in algorithms:
        display_result(r, source, destination)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 10 ─ INPUT VALIDATION
# ══════════════════════════════════════════════════════════════════════════

def get_valid_location(prompt_text):
    """
    Keep prompting until the user enters a valid campus location.
    Case-insensitive matching for user convenience.
    """
    all_locations = list(CAMPUS_GRAPH.keys())

    while True:
        raw = input(colorize(C.YELLOW, f"  {prompt_text}: ")).strip()

        # Case-insensitive match
        matched = next(
            (loc for loc in all_locations if loc.lower() == raw.lower()),
            None
        )

        if matched:
            return matched

        # Not found: show error and list valid options
        print(colorize(C.RED,
            f"\n  ✗  '{raw}' is not a valid location. Please try again."))
        print(colorize(C.DIM, "  Valid locations:"))
        for loc in all_locations:
            print(colorize(C.DIM, f"    • {loc}"))
        print()


def get_algorithm_choice():
    """Prompt user to choose an algorithm. Returns 'BFS', 'UCS', or 'A*'."""
    display_algorithm_menu()
    mapping = {"1": "BFS", "2": "UCS", "3": "A*"}

    while True:
        choice = input(colorize(C.YELLOW, "  Enter choice (1 / 2 / 3): ")).strip()
        if choice in mapping:
            return mapping[choice]
        print(colorize(C.RED, "  ✗  Invalid choice. Please enter 1, 2, or 3."))


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 11 ─ ROUTE SEARCH FLOW
# ══════════════════════════════════════════════════════════════════════════

def run_route_search():
    """
    Full flow for finding a route:
    1. Get source location
    2. Get destination location
    3. Choose algorithm
    4. Run algorithm
    5. Display result
    """
    print_section_header("FIND OPTIMAL ROUTE", C.CYAN)

    display_locations()
    source      = get_valid_location("Enter Source Location")
    destination = get_valid_location("Enter Destination Location")

    # Handle same source and destination
    if source == destination:
        print()
        print(colorize(C.GREEN + C.BOLD,
            "  ✔  You are already at your destination!"))
        print()
        return

    # Choose algorithm
    algo_name = get_algorithm_choice()

    print()
    print(colorize(C.DIM,
        f"  Searching: {source}  →  {destination}  using {algo_name} ..."))
    print()

    # Run chosen algorithm
    if algo_name == "BFS":
        result = bfs(source, destination)
    elif algo_name == "UCS":
        result = ucs(source, destination)
    else:
        result = astar(source, destination)

    display_result(result, source, destination)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 12 ─ COMPARE ALL ALGORITHMS FLOW
# ══════════════════════════════════════════════════════════════════════════

def run_comparison():
    """Get source/destination and run all three algorithms side by side."""
    print_section_header("COMPARE ALL ALGORITHMS", C.MAGENTA)
    display_locations()
    source      = get_valid_location("Enter Source Location")
    destination = get_valid_location("Enter Destination Location")

    if source == destination:
        print(colorize(C.GREEN, "\n  ✔  Already at destination!\n"))
        return

    display_comparison(source, destination)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 13 ─ MAIN PROGRAM LOOP
#  Menu-driven interface that keeps running until user exits.
# ══════════════════════════════════════════════════════════════════════════

def main():
    """
    Entry point. Displays banner and loops through the main menu
    until the user chooses to exit.
    """
    print_banner()

    while True:
        display_main_menu()
        choice = input(colorize(C.YELLOW, "  Enter option (1–5): ")).strip()

        if choice == "1":
            run_route_search()

        elif choice == "2":
            display_locations()

        elif choice == "3":
            display_campus_graph()

        elif choice == "4":
            run_comparison()

        elif choice == "5":
            print()
            print(colorize(C.GREEN + C.BOLD,
                "  Thank you for using Campus Navigation System. Goodbye! 👋"))
            print()
            break

        else:
            print()
            print(colorize(C.RED,
                "  ✗  Invalid option. Please enter a number between 1 and 5."))
            print()


# ── Entry Point ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()