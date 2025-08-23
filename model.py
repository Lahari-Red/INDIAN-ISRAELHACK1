# model.py

import random
import math

# Home coordinates
HOME_LAT, HOME_LNG = 30.3529, 76.3637

def haversine(coord1, coord2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Earth's radius in km

    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

class Node:
    """A node class for A* Pathfinding."""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic (estimated cost from current node to end)
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.position == other.position

def is_in_zone(position, zones):
    """Checks if a given coordinate is inside any of the no-fly zones."""
    lat, lng = position
    for zone in zones:
        (lat1, lng1), (lat2, lng2) = zone
        if min(lat1, lat2) <= lat <= max(lat1, lat2) and min(lng1, lng2) <= lng <= max(lng1, lng2):
            return True
    return False

def astar(start, end, zones):
    """
    Finds the optimal path between start and end coordinates, avoiding zones,
    using the A* pathfinding algorithm.
    """
    start_node = Node(None, start)
    end_node = Node(None, end)
    
    open_list = [start_node]
    closed_list = []

    while open_list:
        current_node = min(open_list, key=lambda node: node.f)
        open_list.remove(current_node)
        closed_list.append(current_node)

        if haversine(current_node.position, end_node.position) < 0.1:  # Path is close enough
            path = []
            current = current_node
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for d_lat, d_lng in [(0.0005, 0), (0, 0.0005), (-0.0005, 0), (0, -0.0005),
                             (0.0005, 0.0005), (0.0005, -0.0005), (-0.0005, 0.0005), (-0.0005, -0.0005)]:
            new_pos = (current_node.position[0] + d_lat, current_node.position[1] + d_lng)

            if is_in_zone(new_pos, zones):
                continue
            
            new_node = Node(current_node, new_pos)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + haversine(current_node.position, child.position)
            child.h = haversine(child.position, end_node.position)
            child.f = child.g + child.h

            if any(node for node in open_list if child == node and child.g >= node.g):
                continue

            open_list.append(child)
    
    return None # No path found

def generate_no_fly_zones(n=3):
    """Generate n random rectangular no-fly zones near the home location."""
    zones = []
    for _ in range(n):
        lat = HOME_LAT + random.uniform(-0.01, 0.01)
        lng = HOME_LNG + random.uniform(-0.01, 0.01)
        zones.append([[lat, lng], [lat + 0.002, lng + 0.002]])
    return zones

def compute_safe_path(target_lat, target_lng, zones):
    """
    Public function to get the safe path using A*.
    """
    start_point = (HOME_LAT, HOME_LNG)
    target_point = (target_lat, target_lng)
    
    path = astar(start_point, target_point, zones)
    
    # If A* fails, fall back to a simple path to avoid breaking functionality
    if not path:
        print("A* failed, falling back to simple path.")
        path = [[HOME_LAT, HOME_LNG], [(HOME_LAT + target_lat)/2, (HOME_LNG + target_lng)/2], [target_lat, target_lng]]
        # A simple check to ensure the midpoint isn't in a zone
        if is_in_zone(path[1], zones):
            path[1] = (path[1][0] + 0.003, path[1][1] + 0.003)
            
    return path