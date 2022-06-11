import os
import unittest
import uuid
import glob

from constants import DEFAULT_ALGORITHM
from server import Server

path = os.path.join(os.getcwd(), 'resources')
id_length = len(uuid.uuid4().__str__() + ".py")

def random_python_file_name():
    return os.path.join(path, uuid.uuid4().__str__() + ".py")


class ExternalAlgorithmTests(unittest.TestCase):

    def test_fetch_algorithm(self):
        files = glob.glob(os.path.join(path, '*'))
        for f in files:
            os.remove(f)
        server = Server()
        file_names = [random_python_file_name(), random_python_file_name(), random_python_file_name()]
        for file_name in file_names:
            f = open(file_name, "x")
            f.close()
        result = server.get_algorithms(path)
        for file_name in file_names:
            if os.path.exists(file_name):
                os.remove(file_name)
        file_names = set(map(lambda full_file_name: full_file_name[-id_length:], file_names))
        self.assertSetEqual(set(result), file_names.union({DEFAULT_ALGORITHM}))

    def test_save_algorithm(self):
        self.assertEqual(True, False)

    def test_run_algorithm(self):
        self.assertEqual(True, False)
