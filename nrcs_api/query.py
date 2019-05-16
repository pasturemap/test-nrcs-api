from typing import Any, Iterable, List

import requests

from nrcs_api import constants
from nrcs_api.forage_estimate import ForageEstimate
from nrcs_api.region import Region


def format_query(regions: Iterable[Region]) -> str:
    """
    Args:
        regions: an iterable of objects that provide a coordinates.wkt property and a .uuid property

    Returns:
        a query (str) to send to the nrcs api
    """
    values = ',\n'.join((
        constants.VALUES_TEMPLATE.format(wkt=x.coordinates.wkt, uuid=x.uuid)
        for x in regions
    ))
    query: str = constants.QUERY_TEMPLATE.format(values=values)
    print(query)
    return query


def interpret_result(json: List[List[Any]]) -> Iterable[ForageEstimate]:
    for x in json:
        paddock_uuid, wkt, forage_low, forage_regular, forage_high = x
        yield ForageEstimate(
            uuid=paddock_uuid,
            coordinates=wkt,
            forage_low=forage_low,
            forage_regular=forage_regular,
            forage_high=forage_high,
        )


def run_query(query: str) -> List[List[Any]]:
    resp = requests.post(constants.API_URL, json={'query': query, 'format': 'json'})
    print('*****************************************')
    print('responding with status %s', resp.status_code)
    print('%s', resp.text)
    return resp.json()['Table']


def estimate_forage(regions: List[Region]) -> List[ForageEstimate]:
    query = format_query(regions)
    raw = run_query(query)
    return list(interpret_result(raw))
