import json
import unittest

from werkzeug.datastructures import FileStorage

from recommendation_system.types.recommendation_types import simulation_data_from_file, simulation_data_from_dict
from tests.resources.data.ExpectedCsv import expected_csv


csv = list(map(lambda entry: simulation_data_from_dict(json.loads(entry)), expected_csv))


class TestCSVLoader(unittest.TestCase):
    def test_csv_loaded_correctly(self):
        with open('resources/data/Example.csv', 'rb') as fp:
            file = FileStorage(fp)
            value = simulation_data_from_file(file)
        self.assertEqual(csv, value)
