from typing import List, TypedDict, Dict
from collections import defaultdict

class Flight(TypedDict):
    from_: str
    to: str
    price: int


def main():
    flights = [
        # East Coast
        {"from_": "NYC", "to": "BOS", "price": 100},  # NYC -> Boston
        {"from_": "BOS", "to": "NYC", "price": 110},  # Boston -> NYC
        {"from_": "NYC", "to": "PHL", "price": 80},   # NYC -> Philadelphia
        {"from_": "PHL", "to": "NYC", "price": 85},   # Philadelphia -> NYC
        
        # West Coast
        {"from_": "LAX", "to": "SFO", "price": 150},  # LA -> San Francisco
        {"from_": "SFO", "to": "LAX", "price": 160},  # San Francisco -> LA
        {"from_": "SEA", "to": "SFO", "price": 180},  # Seattle -> San Francisco
        {"from_": "SFO", "to": "SEA", "price": 190},  # San Francisco -> Seattle
        {"from_": "PDX", "to": "SEA", "price": 100},  # Portland -> Seattle
        {"from_": "SEA", "to": "PDX", "price": 100},  # Seattle -> Portland
        
        # Cross Country
        {"from_": "NYC", "to": "LAX", "price": 250},  # NYC -> LA
        {"from_": "LAX", "to": "NYC", "price": 260},  # LA -> NYC
        {"from_": "BOS", "to": "LAX", "price": 280},  # Boston -> LA
        
        # Mid-points
        {"from_": "CHI", "to": "NYC", "price": 120},  # Chicago -> NYC
        {"from_": "NYC", "to": "CHI", "price": 110},  # NYC -> Chicago
        {"from_": "CHI", "to": "LAX", "price": 200},  # Chicago -> LA
        {"from_": "LAX", "to": "CHI", "price": 210},  # LA -> Chicago
        {"from_": "DEN", "to": "CHI", "price": 150},  # Denver -> Chicago
        {"from_": "CHI", "to": "DEN", "price": 160},  # Chicago -> Denver
        {"from_": "DEN", "to": "LAX", "price": 180},  # Denver -> LA
        {"from_": "LAX", "to": "DEN", "price": 190},  # LA -> Denver
    ]
    
    print("Multiple Layover Tests:")
    print("\nNYC to SEA (all routes):")
    print(find_routes(
        origin="NYC",
        dest="SEA",
        flights=flights,
        max_hops=3
    ))
    
    print("\nNYC to SEA (routes under $600):")
    print(find_routes(
        origin="NYC",
        dest="SEA",
        flights=flights,
        max_price=600,
        max_hops=3
    ))
    
    print("\nNYC to PDX (multiple possible routes):")
    print(find_routes(
        origin="NYC",
        dest="PDX",
        flights=flights,
        max_hops=3
    ))
    
    print("\nPrice Filter Tests:")
    print("\nNYC to LAX (under $300):")
    print(find_routes(
        origin="NYC",
        dest="LAX",
        flights=flights,
        max_price=300
    ))
    
    print("\nNYC to LAX (under $200 - should be empty):")
    print(find_routes(
        origin="NYC",
        dest="LAX",
        flights=flights,
        max_price=200
    ))
    
    print("\nComplex Routes:")
    print("\nNYC to PDX (max 2 stops, under $500):")
    print(find_routes(
        origin="NYC",
        dest="PDX",
        flights=flights,
        max_price=500,
        max_hops=8
    ))
    
    print("\nNYC to PDX (5 stops, money is no object):")
    print(find_routes(
        origin="NYC",
        dest="PDX",
        flights=flights,
        max_price=50000,
        max_hops=5
    ))
    # End Main()


def find_routes(origin: str, dest: str, flights: List[Flight], max_hops: int = 9999999, max_price: int = 90000000000):
    if origin == dest: return []
    
    flight_map: Dict[str, List[Flight]] = defaultdict(list)
    
    for flight in flights:
        flight_map[flight['from_']].append(flight)

    results: List[(List[str], int)] = []
    visited: set[str] = set()
    
    def dfs_helper(route: List[str], current_loc: str, current_price: int, hops_left: int):       
        if (hops_left < 0): return
        
        if (current_loc == dest):
            results.append((route, current_price))
            return
        
        neighbors: List[Flight] = flight_map[current_loc]
        for neighbor in neighbors:
            next_loc = neighbor["to"]
            next_price = neighbor["price"] + current_price
            next_route = route + [next_loc]
            
            if (next_loc not in visited and next_price <= max_price):
                visited.add(next_loc)
                # print(f'Going to... {next_loc}')
                dfs_helper(next_route, next_loc, next_price, hops_left - 1)
                visited.remove(next_loc)
    
    dfs_helper([origin], origin, 0, max_hops)
    results.sort(key= lambda x: x[1])
    
    answer = [{
        "Route": rt[0],
        "Price": rt[1],
        "Stops": len(rt[0]) - 2
    } for rt in results]
  
    return answer

if __name__ == '__main__':
    main()
