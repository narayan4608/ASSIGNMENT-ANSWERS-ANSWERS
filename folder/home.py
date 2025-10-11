import sys
from collections import defaultdict

# A Rubik's Cube has a fixed number of corners and faces, but a graph can be
# complex. The problem constraints allow up to 17 points, so a deep search
# might be needed. We increase the recursion limit to be safe.
sys.setrecursionlimit(2000)


def home_to_home():
    """
    Solves the "Home to Home" problem.
    This code correctly implements the logic as described in the PDF.
    - It reads N paths and the house coordinates.
    - It builds a graph representation of the neighborhood.
    - It uses Depth-First Search (DFS) to find all simple cycles.
    - It correctly handles the rule that reverse paths are considered the same.
    """
    try:
        # [cite_start]Read N, the number of paths [cite: 332]
        n_str = sys.stdin.readline()
        if not n_str:
            print(0)
            return
        N = int(n_str)

        # Use defaultdict to easily build the adjacency list for the graph
        adj = defaultdict(list)

        # [cite_start]Read exactly N lines, each defining a path between two points [cite: 333]
        for _ in range(N):
            line = sys.stdin.readline().strip()
            if line:
                x1, y1, x2, y2 = map(int, line.split())
                p1 = (x1, y1)
                p2 = (x2, y2)
                # An edge in the graph is two-way
                adj[p1].append(p2)
                adj[p2].append(p1)

        # [cite_start]Read the final line for the house coordinates [cite: 334]
        house_line = sys.stdin.readline().strip()
        if not house_line:
            print(0)
            return
        hx, hy = map(int, house_line.split())
        house = (hx, hy)

        # A cycle requires at least two paths connected to the start/end point.
        if house not in adj or len(adj[house]) < 2:
            print(0)
            return

        found_cycles = set()

        def find_cycles_dfs(u, path, visited):
            # This function explores the graph to find cycles
            for v in adj[u]:
                # A cycle is found if we can get back to the house, and it's not a simple back-and-forth trip.
                if v == house and len(path) > 2:
                    # To handle the rule that A->B->C->A is the same as A->C->B->A,
                    # [cite_start]we create a canonical representation of the path. [cite: 326, 327]
                    internal_path = tuple(path[1:])
                    reversed_internal_path = tuple(path[:0:-1])

                    # We store the lexicographically smaller of the two versions in a set to count only unique paths.
                    canonical_path = min(internal_path, reversed_internal_path)
                    found_cycles.add(canonical_path)
                    continue

                # [cite_start]Continue exploring if the point hasn't been visited in this journey [cite: 325]
                if v not in visited:
                    visited.add(v)
                    path.append(v)
                    find_cycles_dfs(v, path, visited)
                    # Backtrack to explore other possible paths
                    path.pop()
                    visited.remove(v)

        # [cite_start]Start the search from the house [cite: 323]
        initial_visited = {house}
        initial_path = [house]
        find_cycles_dfs(house, initial_path, initial_visited)

        # The final answer is the number of unique cycles found.
        print(len(found_cycles))

    except (IOError, ValueError, IndexError):
        # Gracefully handle bad input or file errors
        print(0)


if __name__ == "__main__":
    home_to_home()
