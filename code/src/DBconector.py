import sqlite3
from classes import TPMSsensor
import datetime as dt


class DBOps:
    def __init__(self, DBname : str):
        self.con = sqlite3.connect(DBname)
        self.cur = self.con.cursor()

    def exists_by_id(self, id:str) -> bool:
        res = self.cur.execute("SELECT 1 FROM sensors WHERE id="+id)
        return res.fetchone() is not None
    
    
    def create_sensor(self, sensor:TPMSsensor) -> bool:
        return
    
    def delete_sensor(self, id:str) -> bool:
        return
    
    def append_observation(self, sensor_id:str, tpms_id:str, time: dt.datetime) -> bool:
        return
