import os
import unittest
import uuid
import glob

from werkzeug.datastructures import FileStorage

from constants import DEFAULT_ALGORITHM
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
        self.assertEqual(True, False)
