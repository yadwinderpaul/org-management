from unittest import TestCase, mock
from organizations.adapters import PipedriveAdapter

NAME_KEY = 'NAME_KEY'
URL_KEY = 'URL_KEY'
ADDRESS_KEY = 'ADDRESS_KEY'
COORDINATES_KEY = 'COORDINATES_KEY'

LOGGER = mock.Mock()
CONFIG = {
    'ENDPOINT': 'endpoint',
    'API_TOKEN': 'api-token',
    'DEFAULT_LIMIT': 10,
    'NAME_FIELD_KEY': NAME_KEY,
    'URL_FIELD_KEY': URL_KEY,
    'ADDRESS_FIELD_KEY': ADDRESS_KEY,
    'COORDINATES_FIELD_KEY': COORDINATES_KEY
}
ADAPTER = PipedriveAdapter(CONFIG, {'logger': LOGGER})


class TestSerialization(TestCase):
    def setUp(self):
        self.name = 'NAME'
        self.url = 'URL'
        self.address = 'ADDRESS'
        self.lat = 12.0
        self.lng = 60.0
        self.test_details = {
            'name': self.name,
            'url': self.url,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng
        }
        self.result = ADAPTER._serialize_record(self.test_details)

    def test_existence_of_proper_keys(self):
        self.assertTrue(NAME_KEY in self.result)
        self.assertTrue(URL_KEY in self.result)
        self.assertTrue(ADDRESS_KEY in self.result)
        self.assertTrue(COORDINATES_KEY in self.result)

    def test_existence_of_proper_values(self):
        self.assertTrue(self.result[NAME_KEY] == self.name)
        self.assertTrue(self.result[URL_KEY] == self.url)
        self.assertTrue(self.result[ADDRESS_KEY] == self.address)
        self.assertTrue(
            self.result[COORDINATES_KEY] == f'{self.lat},{self.lng}'
        )


class TestDeserialization(TestCase):
    def setUp(self):
        self.id = 'ID'
        self.name = 'NAME'
        self.url = 'URL'
        self.address = 'ADDRESS'
        self.lat = 12.0
        self.lng = 60.0
        self.test_serialized = {
            'id': self.id,
            NAME_KEY: self.name,
            URL_KEY: self.url,
            ADDRESS_KEY: self.address,
            COORDINATES_KEY: f'{self.lat},{self.lng}'
        }
        self.result = ADAPTER._parse_record({'data': self.test_serialized})

    def test_existence_of_proper_keys(self):
        self.assertTrue('id' in self.result)
        self.assertTrue('name' in self.result)
        self.assertTrue('url' in self.result)
        self.assertTrue('address' in self.result)
        self.assertTrue('lat' in self.result)
        self.assertTrue('lng' in self.result)

    def test_existence_of_proper_values(self):
        self.assertTrue(self.result['id'] == self.id)
        self.assertTrue(self.result['name'] == self.name)
        self.assertTrue(self.result['url'] == self.url)
        self.assertTrue(self.result['address'] == self.address)
        self.assertTrue(self.result['lat'] == self.lat)
        self.assertTrue(self.result['lng'] == self.lng)
