from typing import Any, Dict, Union

import shapely.geometry
import shapely.wkt
from shapely.geometry.base import BaseGeometry


def to_shapely(thing: Union[str, Dict[str, Any]]) -> BaseGeometry:
    if isinstance(thing, dict):
        return shapely.geometry.shape(thing)
    else:
        return shapely.wkt.loads(thing)
