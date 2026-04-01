import datetime as dt

class TPMSsensor:
    def __init__(self, id : int, type : str , observations: dict[int, list[dt.datetime]]):
        self.id: int = id
        self.type: str  = type 
        self.observations: dict[int, list[dt.datetime]] = observations


  