from typing import Optional, Union
from uuid import UUID

from django.contrib.gis.geos import GEOSGeometry


class ForageEstimate:
    """
    a class for storing results from the NRCS query api.
    """
    uuid: UUID
    coordinates: GEOSGeometry
    forage_low: Optional[float]
    forage_regular: Optional[float]
    forage_high: Optional[float]

    def __init__(
            self,
            uuid: Union[str, UUID],
            coordinates: Union[str, GEOSGeometry],
            forage_low: Optional[int] = None,
            forage_regular: Optional[int] = None,
            forage_high: Optional[int] = None
    ) -> None:
        self.uuid = UUID(str(uuid))
        self.coordinates = GEOSGeometry(coordinates)
        self.forage_low = forage_low
        self.forage_regular = forage_regular
        self.forage_high = forage_high
