"""
=============================================================================
        INTELLIGENT CAMPUS NAVIGATION ASSISTANT
        CFAI (Computational Foundations of Artificial Intelligence)
        Mini Project — KL University, Hyderabad

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

import heapq
from collections import deque


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 1 ─ ANSI COLOR CODES
# ══════════════════════════════════════════════════════════════════════════

class C:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BG_DARK = '\033[48;5;234m'
    ORANGE  = '\033[38;5;214m'
    TEAL    = '\033[38;5;43m'
    PURPLE  = '\033[38;5;141m'

def colorize(color_code, text):
    return f"{color_code}{text}{C.RESET}"


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 2 ─ CAMPUS GRAPH
# ══════════════════════════════════════════════════════════════════════════

CAMPUS_GRAPH = {

    "Main Gate": [
        ("Hostel",        10, 8),
        ("Cafeteria",      8, 6),
        ("Parking",        6, 4),
        ("Central Plaza",  5, 3),
        ("Office",         4, 3),
    ],

    "Parking": [
        ("Hostel",    9, 7),
        ("Main Gate", 6, 4),
        ("Ground",    4, 3),
    ],

    "Hostel": [
        ("Parking",   9, 7),
        ("Main Gate", 10, 8),
    ],

    "Cafeteria": [
        ("Central Plaza", 5, 4),
        ("Auditorium",    4, 3),
        ("Library",       4, 3),
        ("Lab",           3, 2),
        ("Medical Room",  2, 2),
        ("Ground",        2, 1),
    ],

    "Auditorium": [
        ("Cafeteria",    4, 3),
        ("Office",       3, 2),
        ("Medical Room", 3, 2),
        ("Library",      2, 2),
    ],

    "Library": [
        ("Cafeteria",    4, 3),
        ("Office",       4, 3),
        ("Medical Room", 2, 2),
        ("Auditorium",   2, 2),
    ],

    "Office": [
        ("Auditorium", 3, 2),
        ("Library",    4, 3),
        ("Main Gate",  4, 3),
        ("Lab",        2, 1),
    ],

    "Medical Room": [
        ("Auditorium", 3, 2),
        ("Library",    2, 2),
        ("Cafeteria",  2, 2),
        ("Lab",        3, 2),
    ],

    "Lab": [
        ("Office",       2, 1),
        ("Medical Room", 3, 2),
    ],

    "Ground": [
        ("Cafeteria", 2, 1),
        ("Parking",   4, 3),
    ],

    "Central Plaza": [
        ("Ground",       3, 2),
        ("Auditorium",   4, 3),
        ("Library",      5, 4),
        ("Cafeteria",    5, 4),
        ("Main Gate",    5, 3),
        ("Office",       6, 4),
    ],
}

# Location icons for display
LOCATION_ICONS = {
    "Main Gate":     "🚪",
    "Parking":       "🅿️ ",
    "Hostel":        "🏠",
    "Cafeteria":     "🍽️ ",
    "Auditorium":    "🎭",
    "Library":       "📚",
    "Office":        "🏢",
    "Medical Room":  "🏥",
    "Lab":           "🔬",
    "Ground":        "⚽",
    "Central Plaza": "🌿",
}


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 3 ─ HEURISTICS FOR A*
# ══════════════════════════════════════════════════════════════════════════

HEURISTICS = {
    "Library": {
        "Library": 0, "Auditorium": 2, "Medical Room": 2,
        "Office": 4, "Cafeteria": 4, "Lab": 5,
        "Central Plaza": 5, "Main Gate": 8, "Ground": 6,
        "Parking": 9, "Hostel": 11,
    },
    "Lab": {
        "Lab": 0, "Office": 2, "Medical Room": 3,
        "Auditorium": 4, "Library": 5, "Cafeteria": 5,
        "Central Plaza": 7, "Main Gate": 6, "Ground": 6,
        "Parking": 8, "Hostel": 10,
    },
    "Hostel": {
        "Hostel": 0, "Parking": 9, "Main Gate": 10,
        "Ground": 12, "Cafeteria": 14, "Central Plaza": 13,
        "Auditorium": 15, "Library": 16, "Office": 14,
        "Medical Room": 16, "Lab": 15,
    },
    "Cafeteria": {
        "Cafeteria": 0, "Ground": 2, "Medical Room": 2,
        "Lab": 3, "Auditorium": 4, "Library": 4,
        "Central Plaza": 5, "Office": 5, "Main Gate": 8,
        "Parking": 6, "Hostel": 14,
    },
    "Central Plaza": {
        "Central Plaza": 0, "Ground": 3, "Cafeteria": 5,
        "Auditorium": 4, "Library": 5, "Office": 6,
        "Main Gate": 5, "Medical Room": 6, "Lab": 7,
        "Parking": 7, "Hostel": 12,
    },
    "Ground": {
        "Ground": 0, "Cafeteria": 2, "Parking": 4,
        "Central Plaza": 3, "Medical Room": 4, "Auditorium": 5,
        "Library": 6, "Lab": 5, "Office": 6,
        "Main Gate": 8, "Hostel": 11,
    },
    "Office": {
        "Office": 0, "Lab": 2, "Auditorium": 3,
        "Library": 4, "Medical Room": 5, "Main Gate": 4,
        "Cafeteria": 5, "Central Plaza": 6, "Ground": 6,
        "Parking": 8, "Hostel": 12,
    },
}

def get_heuristic(node, goal):
    if goal in HEURISTICS and node in HEURISTICS[goal]:
        return HEURISTICS[goal][node]
    return 0


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 4 ─ RESULT DATA STRUCTURE
# ══════════════════════════════════════════════════════════════════════════

class SearchResult:
    def __init__(self, path, total_distance, total_time,
                 nodes_explored, algorithm, found=True):
        self.path           = path
        self.total_distance = total_distance
        self.total_time     = total_time
        self.nodes_explored = nodes_explored
        self.algorithm      = algorithm
        self.found          = found


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 5 ─ PATH COST UTILITY
# ══════════════════════════════════════════════════════════════════════════

def calculate_path_cost(path):
    total_distance = 0
    total_time     = 0
    for i in range(len(path) - 1):
        for (neighbor, dist, t) in CAMPUS_GRAPH.get(path[i], []):
            if neighbor == path[i + 1]:
                total_distance += dist
                total_time     += t
                break
    return total_distance, total_time


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 6 ─ BFS
# ══════════════════════════════════════════════════════════════════════════

def bfs(source, destination):
    if source == destination:
        return SearchResult([source], 0, 0, 1, "BFS")
    queue   = deque([(source, [source])])
    visited = set([source])
    nodes_explored = 0
    while queue:
        current_node, current_path = queue.popleft()
        nodes_explored += 1
        for (neighbor, distance, time) in CAMPUS_GRAPH.get(current_node, []):
            if neighbor not in visited:
                new_path = current_path + [neighbor]
                if neighbor == destination:
                    dist, t = calculate_path_cost(new_path)
                    return SearchResult(new_path, dist, t, nodes_explored + 1, "BFS")
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    return SearchResult([], 0, 0, nodes_explored, "BFS", found=False)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 7 ─ UCS
# ══════════════════════════════════════════════════════════════════════════

def ucs(source, destination):
    if source == destination:
        return SearchResult([source], 0, 0, 1, "UCS")
    priority_queue = [(0, source, [source])]
    visited        = {}
    nodes_explored = 0
    while priority_queue:
        g_cost, current_node, current_path = heapq.heappop(priority_queue)
        nodes_explored += 1
        if current_node in visited and visited[current_node] <= g_cost:
            continue
        visited[current_node] = g_cost
        if current_node == destination:
            dist, t = calculate_path_cost(current_path)
            return SearchResult(current_path, dist, t, nodes_explored, "UCS")
        for (neighbor, distance, time) in CAMPUS_GRAPH.get(current_node, []):
            new_cost = g_cost + distance
            if neighbor not in visited or visited[neighbor] > new_cost:
                heapq.heappush(priority_queue, (new_cost, neighbor, current_path + [neighbor]))
    return SearchResult([], 0, 0, nodes_explored, "UCS", found=False)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 8 ─ A*
# ══════════════════════════════════════════════════════════════════════════

def astar(source, destination):
    if source == destination:
        return SearchResult([source], 0, 0, 1, "A*")
    h_start        = get_heuristic(source, destination)
    priority_queue = [(h_start, 0, source, [source])]
    visited        = {}
    nodes_explored = 0
    while priority_queue:
        f_cost, g_cost, current_node, current_path = heapq.heappop(priority_queue)
        nodes_explored += 1
        if current_node in visited and visited[current_node] <= g_cost:
            continue
        visited[current_node] = g_cost
        if current_node == destination:
            dist, t = calculate_path_cost(current_path)
            return SearchResult(current_path, dist, t, nodes_explored, "A*")
        for (neighbor, distance, time) in CAMPUS_GRAPH.get(current_node, []):
            new_g = g_cost + distance
            new_h = get_heuristic(neighbor, destination)
            new_f = new_g + new_h
            if neighbor not in visited or visited[neighbor] > new_g:
                heapq.heappush(priority_queue, (new_f, new_g, neighbor, current_path + [neighbor]))
    return SearchResult([], 0, 0, nodes_explored, "A*", found=False)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 9 ─ DISPLAY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

WIDTH = 62

def print_banner():
    IW = 58  # inner width — no emojis inside box so padding is exact

    def banner_row(plain_text, colored_text):
        pad = IW - len(plain_text)
        print(colorize(C.CYAN + C.BOLD, "  ║") + colored_text + " " * pad +
              colorize(C.CYAN + C.BOLD, "║"))

    print()
    print(colorize(C.CYAN + C.BOLD, "  ╔" + "═" * IW + "╗"))
    banner_row("", "")
    banner_row(
        "    INTELLIGENT CAMPUS NAVIGATION SYSTEM    ",
        colorize(C.WHITE + C.BOLD, "    INTELLIGENT CAMPUS NAVIGATION SYSTEM    "))
    banner_row(
        "       KL University · Hyderabad Campus     ",
        colorize(C.TEAL, "       KL University · Hyderabad Campus     "))
    banner_row("", "")
    banner_row(
        "       Algorithms: BFS  ·  UCS  ·  A*      ",
        colorize(C.DIM, "       Algorithms: BFS  ·  UCS  ·  A*      "))
    banner_row(
        "       CFAI Mini Project                    ",
        colorize(C.DIM, "       CFAI Mini Project                    "))
    banner_row("", "")
    print(colorize(C.CYAN + C.BOLD, "  ╚" + "═" * IW + "╝"))
    print()


def print_divider(char="─", color=C.DIM):
    print(colorize(color, "  " + char * WIDTH))


def print_section_header(title, icon="", color=C.CYAN):
    print()
    print_divider("─", color)
    pad = (WIDTH - len(title) - len(icon) - 2) // 2
    print(colorize(color + C.BOLD, f"  {'─'*pad}  {icon}{title}  {'─'*pad}"))
    print_divider("─", color)
    print()


def display_main_menu():
    print_section_header("MAIN MENU", "📍 ")
    menu_items = [
        ("1", "🔍", "Find Optimal Route",      C.CYAN),
        ("2", "📋", "View Campus Locations",   C.BLUE),
        ("3", "🗺️ ", "View Campus Graph Map",   C.TEAL),
        ("4", "⚡", "Compare All Algorithms",  C.MAGENTA),
        ("5", "👋", "Exit",                    C.RED),
    ]
    for num, icon, label, col in menu_items:
        bullet = colorize(col + C.BOLD, f"  [{num}]")
        print(f"{bullet}  {icon}  {label}")
    print()
    print_divider()
    print()


def display_locations():
    print_section_header("CAMPUS LOCATIONS", "🏫 ", C.BLUE)
    all_locations = list(CAMPUS_GRAPH.keys())
    for i, loc in enumerate(all_locations, start=1):
        icon   = LOCATION_ICONS.get(loc, "📍")
        num    = colorize(C.YELLOW + C.BOLD, f"  [{i:02}]")
        name   = colorize(C.WHITE, loc)
        edges  = colorize(C.DIM, f"({len(CAMPUS_GRAPH[loc])} connections)")
        print(f"{num}  {icon}  {name}  {edges}")
    print()
    print(colorize(C.DIM, f"  Total: {len(all_locations)} locations  ·  Type exact name to select"))
    print()


def display_campus_graph():
    print_section_header("CAMPUS GRAPH MAP", "🗺️  ", C.TEAL)
    print(colorize(C.DIM, "  Location → Neighbor  [ dist units | time min ]"))
    print()
    for node, edges in CAMPUS_GRAPH.items():
        icon = LOCATION_ICONS.get(node, "📍")
        print(colorize(C.CYAN + C.BOLD, f"  {icon}  {node}"))
        for idx, (neighbor, dist, time) in enumerate(edges):
            is_last  = idx == len(edges) - 1
            branch   = "└──▶" if is_last else "├──▶"
            n_icon   = LOCATION_ICONS.get(neighbor, "📍")
            nbr      = colorize(C.GREEN, f"{neighbor}")
            cost     = colorize(C.YELLOW, f"[ {dist}u | {time}min ]")
            print(colorize(C.DIM, f"     {branch}") + f"  {n_icon}  {nbr}  {cost}")
        print()


def display_algorithm_menu():
    print()
    print(colorize(C.MAGENTA + C.BOLD, "  ┌─ Select Algorithm ───────────────────────────────┐"))
    algos = [
        ("1", "BFS", "Breadth-First Search", "minimizes hops",            C.CYAN),
        ("2", "UCS", "Uniform Cost Search",  "optimal by distance",       C.TEAL),
        ("3", "A*",  "A* Search",            "heuristic-guided optimal",  C.ORANGE),
    ]
    for num, short, full, desc, col in algos:
        n    = colorize(C.YELLOW + C.BOLD, f"  [{num}]")
        algo = colorize(col + C.BOLD, f"{short:<4}")
        name = colorize(C.WHITE, f"{full:<24}")
        d    = colorize(C.DIM, desc)
        print(f"{n}  {algo}  {name}  {d}")
    print(colorize(C.MAGENTA + C.BOLD, "  └───────────────────────────────────────────────────┘"))
    print()


def display_result(result, source, destination):
    algo_colors = {"BFS": C.CYAN, "UCS": C.TEAL, "A*": C.ORANGE}
    col = algo_colors.get(result.algorithm, C.CYAN)

    print()
    print(colorize(col + C.BOLD, "  ╔" + "═" * (WIDTH - 2) + "╗"))
    algo_label = f"  Algorithm : {result.algorithm}"
    print(colorize(col + C.BOLD, "  ║") +
          colorize(col + C.BOLD, f"  {result.algorithm} — ") +
          colorize(C.DIM, {"BFS": "Breadth-First Search",
                           "UCS": "Uniform Cost Search",
                           "A*":  "A* Heuristic Search"}.get(result.algorithm, "")) +
          colorize(col + C.BOLD, " " * (WIDTH - 4 - len(result.algorithm) - 25) + "║"))
    print(colorize(col + C.BOLD, "  ╚" + "═" * (WIDTH - 2) + "╝"))
    print()

    if not result.found or not result.path:
        print(colorize(C.RED + C.BOLD, "  ✗  No path found between the given locations."))
        print()
        return

    # Path display
    src_icon  = LOCATION_ICONS.get(source, "📍")
    dst_icon  = LOCATION_ICONS.get(destination, "📍")
    print(colorize(C.WHITE + C.BOLD, "  Route Found:"))
    print()

    for idx, node in enumerate(result.path):
        icon = LOCATION_ICONS.get(node, "📍")
        if idx == 0:
            tag = colorize(C.GREEN + C.BOLD, " START")
        elif idx == len(result.path) - 1:
            tag = colorize(C.MAGENTA + C.BOLD, "   END")
        else:
            tag = colorize(C.DIM, f"  [{idx}]")

        node_str = colorize(C.WHITE + C.BOLD if idx in (0, len(result.path)-1) else C.WHITE, node)
        print(f"    {tag}  {icon}  {node_str}")

        if idx < len(result.path) - 1:
            # Show edge cost between steps
            for (nb, dist, time) in CAMPUS_GRAPH.get(node, []):
                if nb == result.path[idx + 1]:
                    print(colorize(C.DIM, f"           │  {dist}u · {time}min"))
                    break
            print(colorize(col, "           ▼"))

    print()
    print_divider("·", col)
    print()

    # Stats
    hops = len(result.path) - 1
    stats = [
        ("📏  Distance",     f"{result.total_distance} units",    C.YELLOW),
        ("⏱️   Time",         f"{result.total_time} min",          C.YELLOW),
        ("🔗  Hops",         f"{hops}",                           C.GREEN),
        ("🔎  Nodes Explored", f"{result.nodes_explored}",        C.CYAN),
    ]
    for label, value, vcol in stats:
        lbl = colorize(C.DIM,         f"  {label:<22}")
        val = colorize(vcol + C.BOLD, value)
        print(f"{lbl}  {val}")

    print()
    print_divider("·", col)
    print(colorize(C.GREEN + C.BOLD, "  ✔  Path found successfully"))
    print()


def display_comparison(source, destination):
    print_section_header(f"ALGORITHM COMPARISON", "⚡ ", C.MAGENTA)
    src_icon = LOCATION_ICONS.get(source, "📍")
    dst_icon = LOCATION_ICONS.get(destination, "📍")
    print(colorize(C.WHITE + C.BOLD,
        f"  {src_icon}  {source}   →→→   {dst_icon}  {destination}"))
    print()

    results = [
        bfs(source, destination),
        ucs(source, destination),
        astar(source, destination),
    ]

    algo_colors = {"BFS": C.CYAN, "UCS": C.TEAL, "A*": C.ORANGE}
    algo_descs  = {
        "BFS": "Fewest hops — ignores weights",
        "UCS": "Cheapest cost — weight optimal",
        "A*" : "Heuristic guided — smart & fast",
    }

    # ── Comparison table ──────────────────────────────────────────────────
    print(colorize(C.MAGENTA + C.BOLD,
        "  ╔══════════╦══════════╦══════════╦═══════╦════════════════╗"))
    print(colorize(C.MAGENTA + C.BOLD,
        "  ║ Algo     ║  Dist    ║  Time    ║ Hops  ║ Nodes Explored ║"))
    print(colorize(C.MAGENTA + C.BOLD,
        "  ╠══════════╬══════════╬══════════╬═══════╬════════════════╣"))

    best_dist  = min((r.total_distance for r in results if r.found), default=0)
    best_hops  = min((len(r.path)-1    for r in results if r.found), default=0)
    best_nodes = min((r.nodes_explored for r in results if r.found), default=0)

    for r in results:
        col = algo_colors.get(r.algorithm, C.CYAN)
        if r.found and r.path:
            hops       = len(r.path) - 1
            dist_str   = f"{r.total_distance:<6}"  + ("u ✓" if r.total_distance == best_dist  else "u  ")
            time_str   = f"{r.total_time:<6}"      + "m  "
            hops_str   = f"{hops:<3}"              + ("  ✓" if hops             == best_hops   else "   ")
            nodes_str  = f"{r.nodes_explored:<10}" + ("  ✓" if r.nodes_explored == best_nodes  else "   ")
        else:
            dist_str  = "N/A      "
            time_str  = "N/A      "
            hops_str  = "N/A   "
            nodes_str = "N/A           "

        algo_col = colorize(col + C.BOLD, f" {r.algorithm:<8}")
        print(f"  ║{algo_col}║ "
              f"{colorize(C.YELLOW, dist_str)} ║ "
              f"{colorize(C.YELLOW, time_str)} ║ "
              f"{colorize(C.GREEN,  hops_str)} ║ "
              f"{colorize(C.CYAN,   nodes_str)} ║")

    print(colorize(C.MAGENTA + C.BOLD,
        "  ╚══════════╩══════════╩══════════╩═══════╩════════════════╝"))
    print()
    print(colorize(C.DIM, "  ✓ = best in that category"))
    print()

    # ── Path comparison side by side ──────────────────────────────────────
    print_divider("─", C.MAGENTA)
    print(colorize(C.WHITE + C.BOLD, "  Paths Taken:"))
    print()
    for r in results:
        col  = algo_colors.get(r.algorithm, C.CYAN)
        desc = algo_descs.get(r.algorithm, "")
        print(colorize(col + C.BOLD, f"  {r.algorithm}") +
              colorize(C.DIM, f"  ({desc})"))
        if r.found and r.path:
            path_str = "  →  ".join(
                f"{LOCATION_ICONS.get(n,'📍')} {n}" for n in r.path
            )
            print(f"    {colorize(C.WHITE, path_str)}")
        else:
            print(colorize(C.RED, "    No path found"))
        print()

    # ── Insight ───────────────────────────────────────────────────────────
    print_divider("─", C.DIM)
    print()
    print(colorize(C.YELLOW + C.BOLD, "  💡 Key Insights:"))
    print(colorize(C.DIM, "  · BFS finds the path with fewest hops — ignores edge weights"))
    print(colorize(C.DIM, "  · UCS finds the cheapest path by total distance cost"))
    print(colorize(C.DIM, "  · A* is guided by h(n) — explores fewer nodes than UCS"))
    print(colorize(C.DIM, "  · Lower Nodes Explored = smarter, more efficient search"))
    print()

    # ── Detailed individual results ───────────────────────────────────────
    print_section_header("DETAILED RESULTS", "📋 ", C.CYAN)
    for r in results:
        display_result(r, source, destination)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 10 ─ INPUT VALIDATION
# ══════════════════════════════════════════════════════════════════════════

def get_valid_location(prompt_text):
    all_locations = list(CAMPUS_GRAPH.keys())
    while True:
        raw     = input(colorize(C.YELLOW + C.BOLD, f"\n  ❯ {prompt_text}: ")).strip()
        matched = next((loc for loc in all_locations if loc.lower() == raw.lower()), None)
        if matched:
            icon = LOCATION_ICONS.get(matched, "📍")
            print(colorize(C.GREEN, f"  ✔  Selected: {icon}  {matched}"))
            return matched
        print(colorize(C.RED, f"\n  ✗  '{raw}' not found. Valid locations:"))
        for loc in all_locations:
            icon = LOCATION_ICONS.get(loc, "📍")
            print(colorize(C.DIM, f"     {icon}  {loc}"))


def get_algorithm_choice():
    display_algorithm_menu()
    mapping = {"1": "BFS", "2": "UCS", "3": "A*"}
    while True:
        choice = input(colorize(C.YELLOW + C.BOLD, "  ❯ Enter choice (1 / 2 / 3): ")).strip()
        if choice in mapping:
            return mapping[choice]
        print(colorize(C.RED, "  ✗  Invalid. Enter 1, 2, or 3."))


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 11 ─ ROUTE SEARCH FLOW
# ══════════════════════════════════════════════════════════════════════════

def run_route_search():
    print_section_header("FIND OPTIMAL ROUTE", "🔍 ", C.CYAN)
    display_locations()
    source      = get_valid_location("Enter Source Location")
    destination = get_valid_location("Enter Destination Location")

    if source == destination:
        print()
        print(colorize(C.GREEN + C.BOLD, "  ✔  You are already at your destination!"))
        print()
        return

    algo_name = get_algorithm_choice()
    print()
    print(colorize(C.DIM, f"  Searching ...  {source}  →  {destination}  [{algo_name}]"))
    print()

    if   algo_name == "BFS": result = bfs(source, destination)
    elif algo_name == "UCS": result = ucs(source, destination)
    else:                    result = astar(source, destination)

    display_result(result, source, destination)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 12 ─ COMPARE ALL ALGORITHMS
# ══════════════════════════════════════════════════════════════════════════

def run_comparison():
    print_section_header("COMPARE ALL ALGORITHMS", "⚡ ", C.MAGENTA)
    display_locations()
    source      = get_valid_location("Enter Source Location")
    destination = get_valid_location("Enter Destination Location")

    if source == destination:
        print(colorize(C.GREEN, "\n  ✔  Already at destination!\n"))
        return

    display_comparison(source, destination)


# ══════════════════════════════════════════════════════════════════════════
#  SECTION 13 ─ MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════

def main():
    print_banner()

    while True:
        display_main_menu()
        choice = input(colorize(C.YELLOW + C.BOLD, "  ❯ Enter option (1–5): ")).strip()

        if   choice == "1": run_route_search()
        elif choice == "2": display_locations()
        elif choice == "3": display_campus_graph()
        elif choice == "4": run_comparison()
        elif choice == "5":
            print()
            print_divider("═", C.CYAN)
            print(colorize(C.CYAN + C.BOLD,
                "  👋  Thank you for using Campus Navigation System!"))
            print(colorize(C.DIM,
                "      KL University, Hyderabad  ·  CFAI Project"))
            print_divider("═", C.CYAN)
            print()
            break
        else:
            print(colorize(C.RED, "\n  ✗  Invalid option. Enter 1–5.\n"))


if __name__ == "__main__":
    main()
