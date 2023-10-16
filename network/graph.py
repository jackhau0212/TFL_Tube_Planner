class NeighbourGraphBuilder:
    """
    Task 2: Complete the definition of the NeighbourGraphBuilder class by:
    - completing the "build" method below (don't hesitate to divide your code 
      into several sub-methods, if needed)
    """

    def __init__(self):
        pass

    def find_neighbouring_stations(self, station, tubemap):
        neighbouring_stations = set()
        
        connections = tubemap.connections
        
        for connection in connections:
            if station in connection.stations:
                neighbouring_stations.update(connection.stations)
                
        neighbouring_stations.remove(station)
        
        return neighbouring_stations

    def build(self, tubemap):
        """ Builds a graph encoding neighbouring connections between stations.

        ----------------------------------------------

        The returned graph should be a dictionary having the following form:
        {
            "station_A_id": {
                "neighbour_station_1_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],

                "neighbour_station_2_id": [
                                connection_1 (instance of Connection),
                                connection_2 (instance of Connection),
                                ...],
                ...
            }

            "station_B_id": {
                ...
            }

            ...

        }

        ----------------------------------------------

        For instance, knowing that the id of "Hammersmith" station is "110",
        graph['110'] should be equal to:
        {
            '17': [
                Connection(Hammersmith<->Barons Court, District Line, 1),
                Connection(Hammersmith<->Barons Court, Piccadilly Line, 2)
                ],

            '209': [
                Connection(Hammersmith<->Ravenscourt Park, District Line, 2)
                ],

            '101': [
                Connection(Goldhawk Road<->Hammersmith, Hammersmith & City Line, 2)
                ],

            '265': [
                Connection(Hammersmith<->Turnham Green, Piccadilly Line, 2)
                ]
        }

        ----------------------------------------------

        Args:
            tubemap (TubeMap) : tube map serving as a reference for building 
                the graph.

        Returns:
            graph (dict) : as described above. 
                If the input data (tubemap) is invalid, 
                the method should return an empty dict.
        """
        
        graph = dict()
        
        for tube_id in tubemap.stations:
            
            neighbouring_stations = self.find_neighbouring_stations(station=tubemap.stations[tube_id], tubemap=tubemap)
            
            station_dict = dict()
            
            for neighbouring_station in neighbouring_stations:
                station_dict[neighbouring_station.id] = []
            
            
            for connection in tubemap.connections:
                if tubemap.stations[tube_id] in connection.stations:
                    neighbouring_station_id = list(connection.stations)
                    neighbouring_station_id.remove(tubemap.stations[tube_id])
                    station_dict[neighbouring_station_id[0].id].append(connection)
            
            graph[tube_id] = station_dict
        
        return graph


def test_graph():
    from tube.map import TubeMap
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")

    graph_builder = NeighbourGraphBuilder()
    graph = graph_builder.build(tubemap)

    print(tubemap.stations["89"])
    print(graph["89"])


if __name__ == "__main__":
    test_graph()

    
