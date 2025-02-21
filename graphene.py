from collections import defaultdict
from typing import Dict, Set, List, Tuple, Optional
from queue import PriorityQueue

class Graph:
    def __init__(self):
        # Format: vertex -> {neighbor -> weight}
        self.adjacency: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.vertices: Set[str] = set()
        
    def add_edge(self, v1: str, v2: str, weight: float = 1.0) -> bool:
        """Adds an undirected edge between v1 and v2 with given weight"""
        if v1 == v2:
            return False  # No self-loops
            
        # Add vertices to set
        self.vertices.add(v1)
        self.vertices.add(v2)
        
        # Add edges in both directions
        self.adjacency[v1][v2] = weight
        self.adjacency[v2][v1] = weight
        return True
        
    def remove_vertex(self, vertex: str) -> bool:
        """Removes a vertex and all its edges"""
        if vertex not in self.vertices:
            return False
            
        # Remove all edges to this vertex
        for neighbor in self.adjacency[vertex]:
            del self.adjacency[neighbor][vertex]
            
        # Remove vertex itself
        del self.adjacency[vertex]
        self.vertices.remove(vertex)
        return True
        
    def find_shortest_path(self, start: str, end: str) -> Tuple[Optional[List[str]], float]:
        """Returns (path, total_weight) using Dijkstra's algorithm"""
        if start not in self.vertices or end not in self.vertices:
            return None, float('inf')
            
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start] = 0
        previous = {vertex: None for vertex in self.vertices}
        
        pq = PriorityQueue()
        pq.put((0, start))
        
        while not pq.empty():
            current_distance, current = pq.get()
            
            if current == end:
                break
                
            if current_distance > distances[current]:
                continue
                
            for neighbor, weight in self.adjacency[current].items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    pq.put((distance, neighbor))
        
        # Reconstruct path
        if distances[end] == float('inf'):
            return None, float('inf')
            
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
            
        return path[::-1], distances[end]
        
    def find_bridges(self) -> List[Tuple[str, str]]:
        """Returns list of edges that are bridges (their removal disconnects the graph)"""
        bridges = []
        visit_time = {vertex: 0 for vertex in self.vertices}
        lowest_time = {vertex: 0 for vertex in self.vertices}
        time = [0]  # List to allow modification in nested function
        
        def dfs(vertex: str, parent: Optional[str]) -> None:
            time[0] += 1
            visit_time[vertex] = lowest_time[vertex] = time[0]
            
            for neighbor in self.adjacency[vertex]:
                if neighbor == parent:
                    continue
                    
                if visit_time[neighbor] == 0:
                    dfs(neighbor, vertex)
                    lowest_time[vertex] = min(lowest_time[vertex], lowest_time[neighbor])
                    
                    if lowest_time[neighbor] > visit_time[vertex]:
                        bridges.append((vertex, neighbor))
                else:
                    lowest_time[vertex] = min(lowest_time[vertex], visit_time[neighbor])
        
        for vertex in self.vertices:
            if visit_time[vertex] == 0:
                dfs(vertex, None)
                
        return bridges


def main():
    # Create a sample graph
    g = Graph()
    
    # Add some edges to create a small network
    edges = [
        ("A", "B", 4.0),
        ("B", "C", 3.0),
        ("C", "D", 2.0),
        ("D", "E", 1.0),
        ("A", "D", 5.0),
        ("B", "E", 3.0),
    ]
    
    for v1, v2, weight in edges:
        g.add_edge(v1, v2, weight)
    
    # Test shortest path
    path, distance = g.find_shortest_path("A", "E")
    print(f"Shortest path from A to E: {path}")
    print(f"Total distance: {distance}")
    
    # Find bridges
    bridges = g.find_bridges()
    print(f"Bridges in graph: {bridges}")
    
    # Remove a vertex and check impact
    g.remove_vertex("C")
    new_path, new_distance = g.find_shortest_path("A", "E")
    print(f"New shortest path after removing C: {new_path}")
    print(f"New distance: {new_distance}")


if __name__ == "__main__":
    main()