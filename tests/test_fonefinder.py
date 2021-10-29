import unittest
from fonefinder import FoneFinder, INVALID_US_NUMBER, NO_RECORDS_FOUND
from unittest.mock import patch

test_data = {
    'happy_path': {
        'fixture_file': 'tests/fixtures/successful_lookup.txt',
        'number': '4152342345',
        'status_code': 200,
    },
    'failed_lookup': {
        'fixture_file': 'tests/fixtures/failed_lookup.txt',
        'number': '09702134324',
        'status_code': 200,
    }
}


class TestFoneFinder(unittest.TestCase):

    @patch('requests.get')
    def test_us_phone(self, mock_get):
        input_data = test_data['happy_path']
        mock_get.return_value.status_code = input_data['status_code']
        mock_get.return_value.content = open(input_data['fixture_file'], "r").read()
        us_number = FoneFinder(input_data['number']).info
        self.assertEqual(us_number["state"], 'California')

    @patch('requests.get')
    def test_intl_phone(self, mock_get):
        input_data = test_data['failed_lookup']
        mock_get.return_value.status_code = input_data['status_code']
        mock_get.return_value.content = open(input_data['fixture_file'], "r").read()
        with self.assertRaises(ValueError) as error:
            FoneFinder(input_data['number']).info
            self.assertEqual(error.exception.message, INVALID_US_NUMBER)

    @patch('requests.get')
    def test_no_records_found(self, mock_get):
        input_data = test_data['failed_lookup']
        mock_get.return_value.status_code = input_data['status_code']
        mock_get.return_value.content = open(input_data['fixture_file'], "r").read()
        with self.assertRaises(ValueError) as error:
            FoneFinder(input_data['number']).info
            self.assertEqual(error.exception.message, NO_RECORDS_FOUND)


if __name__ == '__main__':
    unittest.main()
