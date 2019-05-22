from http import HTTPStatus
from typing import Any, List

import geopandas
import pandas as pd
import requests
import shapely.wkt

from nrcs_api import constants


def format_query(regions: pd.DataFrame) -> str:
    """
    Args:
        regions: an iterable of objects that provide a coordinates.wkt property and a .uuid property

    Returns:
        a query (str) to send to the nrcs api
    """
    values = ',\n'.join((
        constants.VALUES_TEMPLATE.format(wkt=x['coordinates'].wkt, uuid=x['uuid'])
        for i, x in regions.iterrows()
    ))
    return constants.QUERY_TEMPLATE.format(values=values)


def interpret_result(json: List[List[Any]]) -> geopandas.GeoDataFrame:
    data = pd.DataFrame(
        json,
        columns=('paddock_uuid', 'coordinates', 'forage_low', 'forage_regular', 'forage_high')
    )
    for col in ('forage_low', 'forage_regular', 'forage_high'):
        data[col] = pd.to_numeric(data[col])
    data['coordinates'] = data['coordinates'].apply(shapely.wkt.loads)
    return geopandas.GeoDataFrame(data, geometry='coordinates', crs='+init=epsg:4326')


def run_query(query: str) -> List[List[Any]]:
    resp = requests.post(constants.API_URL, json={'query': query, 'format': 'json'})
    if resp.status_code != HTTPStatus.OK:
        raise ValueError('query failed! {}'.format(resp.text))
    return resp.json()['Table']


def estimate_forage(regions: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
    query = format_query(regions)
    raw = run_query(query)
    return interpret_result(raw)
