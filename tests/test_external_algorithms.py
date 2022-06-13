import os
import unittest
import uuid
import glob
from random import randint

from werkzeug.datastructures import FileStorage

from constants import DEFAULT_ALGORITHM
from recommendation_system.algorithm_impl.custom_algorithm import CustomAlgorithm
from recommendation_system.types.recommendation_types import simulation_data_from_file
from server import Server

path = os.path.join(os.getcwd(), 'resources', 'data', 'path_for_files')
id_length = len(uuid.uuid4().__str__() + ".py")


def random_python_file_name():
    return os.path.join(path, uuid.uuid4().__str__() + ".py")


def create_file(file_name):
    f = open(file_name, "x")
    f.close()


class ExternalAlgorithmTests(unittest.TestCase):

    def test_fetch_algorithm(self):
        files = glob.glob(os.path.join(path, '*'))
        for f in files:
            os.remove(f)
        server = Server()
        file_names = [random_python_file_name(), random_python_file_name(), random_python_file_name()]
        [create_file(file_name) for file_name in file_names]
        result = server.get_algorithms(path)
        for file_name in file_names:
            if os.path.exists(file_name):
                os.remove(file_name)
        file_names = set(map(lambda full_file_name: full_file_name[-id_length:], file_names))
        self.assertSetEqual(set(result), file_names.union({DEFAULT_ALGORITHM}))

    def test_save_algorithm(self):
        server = Server()
        file_name = random_python_file_name()
        create_file(file_name)
        with open(file_name) as fp:
            fs = FileStorage(fp)
            server.upload_algorithm(fs, path)
            files = glob.glob(os.path.join(path, '*'))
            self.assertTrue(any(map(lambda file: file == file_name, files)))
        files = glob.glob(os.path.join(path, '*'))
        for f in files:
            os.remove(f)

    def test_run_algorithm(self):
        set_point = randint(1, 100)
        csv_path = os.path.join(os.getcwd(), 'resources', 'data', 'Example.csv')
        algo_path = os.path.join(os.getcwd(), 'resources', 'mocks', 'mock_algorithm.py')
        with open(csv_path, 'rb') as fp:
            file = FileStorage(fp)
            data = simulation_data_from_file(file)
        result = CustomAlgorithm(algo_path).recommend(data, set_point)
        self.assertEqual(result.p, set_point)
        self.assertEqual(result.i, data[0].pid_value)
        self.assertEqual(result.d, data[0].process_value)
