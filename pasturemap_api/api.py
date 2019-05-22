from http import HTTPStatus
from uuid import UUID

import geopandas
import pandas as pd
import requests
import shapely.geometry

from pasturemap_api import constants
from pasturemap_api.user import User


def login(email: str, password: str) -> User:
    resp = requests.post(
        '{}/v1/user/login'.format(constants.API_URL),
        json={'email': email, 'password': password},
    )
    if resp.status_code != HTTPStatus.OK:
        raise ValueError('login not successful: {}'.format(resp.text))
    data = resp.json()
    return User(**data)


def masquerade(admin_user: User, masquerade_email: str) -> User:
    resp = requests.post(
        '{}/v1/user/masquerade'.format(constants.API_URL),
        json={'email': masquerade_email, 'admin_password': admin_user.password},
        headers={'Authorization': 'Token {}'.format(admin_user.token)},
    )
    if resp.status_code != HTTPStatus.OK:
        raise ValueError('masquerade not successful for user: {}. Error: {}'.format(masquerade_email, resp.text))
    data = resp.json()
    return User(
        token=data['token'],
        email=masquerade_email,
        password=admin_user.password,
    )


def paddocks(user: User) -> geopandas.GeoDataFrame:
    if user.ranch_uuid is None:
        resp = requests.get(
            '{}/v1/user/me?include_multiple_ranches=true'.format(constants.API_URL),
            headers={'Authorization': 'Token {}'.format(user.token)}
        )
        if resp.status_code != HTTPStatus.OK:
            raise ValueError('could not fetch user information for: {}. Error: {}'.format(user.email, resp.text))
        data = resp.json()
        ranch_uuid = UUID(data['ranches'][0]['ranch_uuid'])
        user.ranch_uuid = ranch_uuid

    resp = requests.get(
        '{}/v1/ranch/{}/paddock/'.format(constants.API_URL, user.ranch_uuid),
        headers={'Authorization': 'Token {}'.format(user.token)},
    )
    if resp.status_code != HTTPStatus.OK:
        raise ValueError('could not fetch paddocks for user: {}. Error: {}'.format(user.email, resp.text))
    data = pd.DataFrame(resp.json())
    data = data[~data['deleted'] & data['is_active'] & data['parent_paddock_uuid'].isnull()]
    data['coordinates'] = data['coordinates'].apply(shapely.geometry.shape)
    data = data[['coordinates', 'uuid', 'identification']]
    return geopandas.GeoDataFrame(data, geometry='coordinates', crs='+init=epsg:4326')
