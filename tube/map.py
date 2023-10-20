import json
from json.decoder import JSONDecodeError
from tube.components import Station, Line, Connection


class TubeMap:
    """
    Task 1: Complete the definition of the TubeMap class by:
    - completing the "import_from_json()" method

    Don't hesitate to divide your code into several sub-methods, if needed.

    As a minimum, the TubeMap class must contain these three member attributes:
    - stations: a dictionary that indexes Station instances by their id 
      (key=id (str), value=Station)
    - lines: a dictionary that indexes Line instances by their id 
      (key=id, value=Line)
    - connections: a list of Connection instances for the TubeMap 
      (list of Connections)
    """

    def __init__(self):
        self.stations = {}  # key: id (str), value: Station instance
        self.lines = {}  # key: id (str), value: Line instance
        self.connections = []  # list of Connection instances

    def import_from_json(self, filepath):
        """ Import tube map information from a JSON file.
        
        During the import process, the `stations`, `lines` and `connections` 
        attributes should be updated.

        You can use the `json` python package to easily load the JSON file at 
        `filepath`

        Note: when the indicated zone is not an integer (for instance: "2.5"), 
            it means that the station belongs to two zones. 
            For example, if the zone of a station is "2.5", 
            it means that the station is in both zones 2 and 3.

        Args:
            filepath (str) : relative or absolute path to the JSON file 
                containing all the information about the tube map graph to 
                import. If filepath is invalid, no attribute should be updated, 
                and no error should be raised.

        Returns:
            None
        """
        try:
            with open(filepath, "r") as jsonfile:
                data = json.load(jsonfile)

            # Importing stations data 
            for station in data["stations"]:
                
                zone_number = float(station["zone"])
                
                # If the station is an integer, this means that the station only belongs to 1 zone
                if zone_number.is_integer():
                    self.stations[station["id"]] = Station(id=station["id"], name=station["name"], zones=int(station["zone"]))
                
                # If the station is not an integer, but a float, this means that the station belongs to 2 zones
                else:
                    zones_set = {int(zone_number), int(zone_number) + 1}
                    self.stations[station["id"]] = Station(id=station["id"], name=station["name"], zones=zones_set)
            
            # Importing lines data
            for line in data["lines"]:
                self.lines[line["line"]] = Line(id=line["line"], name=line["name"])
            
            # Importing conecctions data
            for connection in data["connections"]:
                stations_set = {self.stations.get(connection["station1"]), self.stations.get(connection["station2"])}
                line = self.lines.get(connection["line"])
                self.connections.append(Connection(stations=stations_set, line=line, time=int(connection["time"])))
    
        except FileNotFoundError:
            pass
        
        except JSONDecodeError:
            pass
        
        return


def test_import():
    tubemap = TubeMap()
    tubemap.import_from_json("data/london.json")
    
    # view one example Station
    print(tubemap.stations[list(tubemap.stations)[0]])
    
    # view one example Line
    print(tubemap.lines[list(tubemap.lines)[0]])
    
    # view the first Connection
    print(tubemap.connections[0])
    
    # view stations for the first Connection
    print([station for station in tubemap.connections[0].stations])


if __name__ == "__main__":
    test_import()
    
