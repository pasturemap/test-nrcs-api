import json
from typing import Union
from uuid import UUID

from django.contrib.gis.geos import GEOSGeometry


class Region:
    uuid: UUID
    coordinates: GEOSGeometry

    def __init__(self, uuid: Union[str, UUID], coordinates: Union[str, GEOSGeometry]):
        self.uuid = UUID(str(uuid))

        if isinstance(coordinates, dict):
            coordinates = json.dumps(coordinates)

        self.coordinates = GEOSGeometry(coordinates)
