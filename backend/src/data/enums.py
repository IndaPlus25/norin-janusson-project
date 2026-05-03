from enum import Enum


class EPSG(int, Enum):
    # 4326 / WGS84 is the standard for raw GPS lat/lng.
    STANDARD = 4326
    WEB_MERCATOR = 3857
    SWEREF99_TM = 3006
    ETRS89 = 4258
