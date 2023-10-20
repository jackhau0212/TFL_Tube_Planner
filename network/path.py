from network.graph import NeighbourGraphBuilder

class PathFinder:
    """
    Task 3: Complete the definition of the PathFinder class by:
    - completing the definition of the __init__() method (if needed)
    - completing the "get_shortest_path()" method (don't hesitate to divide 
      your code into several sub-methods)
    """

    def __init__(self, tubemap):
        """
        Args:
            tubemap (TubeMap) : The TubeMap to use.
        """
        self.tubemap = tubemap

        graph_builder = NeighbourGraphBuilder()
        self.graph = graph_builder.build(self.tubemap)
        
    
    def find_station_id_from_name(self, station_name):
        """
        Find the station id from the string name

        Args:
            station_name (string): name of the station

        Returns:
            string: station id
        """
        station_id = ""
        
        for station in self.tubemap.stations:
            if self.tubemap.stations[station].name == station_name:
                station_id = station
                break
            
        return station_id
        
    def get_shortest_path(self, start_station_name, end_station_name):
        """ Find ONE shortest path from start_station_name to end_station_name.
        
        The shortest path is the path that takes the least amount of time.

        For instance, get_shortest_path('Stockwell', 'South Kensington') 
        should return the list:
        [Station(245, Stockwell, {2}), 
         Station(272, Vauxhall, {1, 2}), 
         Station(198, Pimlico, {1}), 
         Station(273, Victoria, {1}), 
         Station(229, Sloane Square, {1}), 
         Station(236, South Kensington, {1})
        ]

        If start_station_name or end_station_name does not exist, return None.
        
        You can use the Dijkstra algorithm to find the shortest path from
        start_station_name to end_station_name.

        Find a tutorial on YouTube to understand how the algorithm works, 
        e.g. https://www.youtube.com/watch?v=GazC3A4OQTE
        
        Alternatively, find the pseudocode on Wikipedia: https://en.wikipedia.org/wiki/Dijkstra's_algorithm#Pseudocode

        Args:
            start_station_name (str): name of the starting station
            end_station_name (str): name of the ending station

        Returns:
            list[Station] : list of Station objects corresponding to ONE 
                shortest path from start_station_name to end_station_name.
                Returns None if start_station_name or end_station_name does not 
                exist.
                Returns a list with one Station object (the station itself) if 
                start_station_name and end_station_name are the same.
        """
        
        if not self.find_station_id_from_name(start_station_name) in self.tubemap.stations and \
            not self.find_station_id_from_name(end_station_name) in self.tubemap.stations:
            return None
        
        # Create a dictionary to store the distance from the start station to each node
        distance = {node: float("infinity") for node in self.graph}
        
        # Create a dictionary to store the previous node in the shortest path
        previous = {node: None for node in self.graph}
        
        # The distance of the start station is 0 because we are starting from this start station
        start_station_id = self.find_station_id_from_name(start_station_name)
        distance[start_station_id] = 0
        
        # Storing all the unvisted stations here
        unvisted_stations = list(self.graph)
        
        while unvisted_stations:
            
            # Need to find the starting fixed station
            
            # Find out the stations that are in the distance that have been visited
            unvisited_distance_intersection = set(distance) - set(unvisted_stations)
            unvisited_distance = distance
            
            # Remove the stations from unvisited_distance dictionary that have been visited
            for i in unvisited_distance_intersection:
                unvisited_distance.pop(i)
            
            # Find out the station in the unvisited_distance dictionary with the lowest distance value
            fixed_station_id = min(unvisited_distance, key=unvisited_distance.get)
            
            # Remove the fixed station from unvisited_stations because we are currently on it
            unvisted_stations.remove(fixed_station_id)
            
            # Find out the stations that are connected to the fixed station which are unvisited
            unvisted_connected_stations = [connected_station for connected_station in self.graph[fixed_station_id] if connected_station in unvisted_stations]
            
            # Looping through all the unvisited_connected_stations
            for unvisited_connected_station in unvisted_connected_stations:
                
                shortest = float("infinity")
                
                # Finding out the quickest way between 2 stations
                # Taking into account of stations that have multiple connections
                for connection in self.graph[fixed_station_id][unvisited_connected_station]:
                    if connection.time < shortest:
                        shortest = connection.time
                
                alt = distance[fixed_station_id] + shortest
                
                # Update the distance dictionary if a more optimal route is found
                if alt < distance[unvisited_connected_station]:
                    distance[unvisited_connected_station] = alt
                    previous[unvisited_connected_station] = self.tubemap.stations[fixed_station_id]
        
        # Creating a list of stations of the route
        route = []
        target_station_id = self.find_station_id_from_name(end_station_name)
        
        if previous[target_station_id] != None or target_station_id == start_station_id:
            while target_station_id != None:
                route.insert(0, self.tubemap.stations[target_station_id])
                if start_station_id == target_station_id:
                    break
                target_station_id = previous[target_station_id].id

        return route


def test_shortest_path():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    path_finder = PathFinder(tubemap)
    stations = path_finder.get_shortest_path("Covent Garden", "Green Park")
    print(stations)
    
    station_names = [station.name for station in stations]
    expected = ["Covent Garden", "Leicester Square", "Piccadilly Circus", 
                "Green Park"]
    assert station_names == expected

if __name__ == "__main__":
    test_shortest_path()