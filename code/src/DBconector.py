import sqlite3
from classes import TPMSsensor
import datetime as dt


class DBOps:
    def __init__(self, DBname : str):
        self.con = sqlite3.connect(DBname)

    def exists_by_id(self, id:str):
        return
    
    
    def create_sensor(self, sensor:TPMSsensor):
        return
    
    def delete_sensor(self, id:str):
        return
    
    def append_observation(self, sensor_id:str, tpms_id:str, time: dt.datetime):
        return
