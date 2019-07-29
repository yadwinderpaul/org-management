from unittest import TestCase, mock
from organizations import Organizations


class TestOrganizations(TestCase):
    def setUp(self):
        mock_config = {'ADAPTER_NAME': 'pipedrive'}
        mock_logger = mock.Mock()
        self.mock_adapter = mock.Mock()
        self.mock_adapter.list_organizations.return_value = [{
            'name': 'Foo'
        }]
        mock_app = {
            'config': mock_config,
            'logger': mock_logger,
            'organizations_adapter': self.mock_adapter
        }

        self.service = Organizations(mock_app)

    def test_list_calls_adapter_fn(self):
        self.service.list()
        self.assertTrue(self.mock_adapter.list_organizations.called)
