import functools
import requests
from haversine import haversine
from .base import BaseAdapter
from organizations.exceptions import\
    OrganizationsException,\
    AbsentResourceException,\
    UnavailableException


def handle_pipedrive_exceptions(fun):
    @functools.wraps(fun)
    def func(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except requests.HTTPError as ex:
            code = ex.response.status_code
            if code in [404, 410]:
                raise AbsentResourceException(original=ex)
            else:
                raise UnavailableException(original=ex)
        except requests.RequestException as ex:
            raise OrganizationsException(original=ex)
    return func


class PipedriveAdapter(BaseAdapter):
    def __init__(self, config, services):
        self._config = config
        self._logger = services['logger']

        self._api_token = self._config['API_TOKEN']
        self._default_limit = self._config['DEFAULT_LIMIT']
        self._keys = {
            'name': self._config['NAME_FIELD_KEY'],
            'url': self._config['URL_FIELD_KEY'],
            'address': self._config['ADDRESS_FIELD_KEY'],
            'coordinates': self._config['COORDINATES_FIELD_KEY']
        }

        self._conn = requests.Session()
        self._conn.params = {'api_token': self._api_token}
        self._base_endpoint = self._config['ENDPOINT']

    @handle_pipedrive_exceptions
    def list_organizations(self, start):
        params = {
            'start': start,
            'limit': self._default_limit
        }

        result = self._conn.get(self._base_endpoint, params=params)
        result.raise_for_status()
        payload = result.json()
        collection = self._parse_collection(payload)
        return collection

    @handle_pipedrive_exceptions
    def get_organization(self, id):
        result = self._conn.get(f'{self._base_endpoint}/{id}')
        result.raise_for_status()
        payload = result.json()
        record = self._parse_record(payload)
        return record

    @handle_pipedrive_exceptions
    def create_organizations(self, details):
        data = self._serialize_record(details)
        self._logger.debug(f'POST data: {data}')
        result = self._conn.post(self._base_endpoint,
                                 json=data)
        result.raise_for_status()
        payload = result.json()
        record = self._parse_record(payload)
        return record

    @handle_pipedrive_exceptions
    def update_organizations(self, id, details):
        data = self._serialize_record(details)
        self._logger.debug(f'PUT data: {data}')
        result = self._conn.put(f'{self._base_endpoint}/{id}',
                                json=data)
        result.raise_for_status()
        payload = result.json()
        record = self._parse_record(payload)
        return record

    @handle_pipedrive_exceptions
    def delete_organizations(self, id):
        result = self._conn.delete(f'{self._base_endpoint}/{id}')
        result.raise_for_status()
        return True

    @handle_pipedrive_exceptions
    def search_organizations(self, query, lat, lng, start):
        params = {
            'term': query,
            'start': start,
            'limit': self._default_limit
        }

        result = self._conn.get(f'{self._base_endpoint}/find',
                                params=params)
        result.raise_for_status()
        payload = result.json()
        collection = self._parse_collection(payload)
        if collection['data'] is not None and\
                lat is not None and lng is not None:
            collection['data'] =\
                self._sort_by_coordinates(collection['data'], lat, lng)
        return collection

    def _serialize_record(self, details):
        return {
            self._keys['name']: details['name'],
            self._keys['url']: details['url'],
            self._keys['address']: details['address'],
            self._keys['coordinates']: ','.join([
                str(details['lat']), str(details['lng'])
            ])
        }

    def _parse_record(self, payload):
        name = None
        url = None
        address = None
        lat = None
        lng = None

        record = payload['data']

        if self._keys['name'] in record:
            name = record[self._keys['name']]
        if self._keys['name'] in record:
            url = record[self._keys['name']]
        if self._keys['name'] in record:
            address = record[self._keys['name']]
        if self._keys['coordinates'] in record and\
                record[self._keys['coordinates']] is not None:
            coordinates = record[self._keys['coordinates']].split(',')
            if len(coordinates) == 2:
                lat = float(coordinates[0])
                lng = float(coordinates[1])
        return {
            'id': record['id'],
            'name': name,
            'url': url,
            'address': address,
            'lat': lat,
            'lng': lng
        }

    def _parse_collection(self, payload):
        data = []
        meta = {}
        if payload is not None:
            if 'data' in payload and payload['data'] is not None:
                records = payload['data']
                data = [
                    self._parse_record({'data': record})
                    for record in records
                ]
            if 'additional_data' in payload and\
                    'pagination' in payload['additional_data']:
                pagination = payload['additional_data']['pagination']
                meta = {
                    'start': pagination['start'],
                    'limit': pagination['limit']
                }
        return {
            'data': data,
            'meta': meta
        }

    def _sort_by_coordinates(self, records, lat, lng):
        def sorter(elem):
            dist = 0
            if elem['lat'] and elem['lng']:
                dist = haversine((lat, lng),
                                 (elem['lat'], elem['lng']))
            return dist
        sorted_records = records.copy()
        sorted_records.sort(key=sorter)
        return sorted_records
