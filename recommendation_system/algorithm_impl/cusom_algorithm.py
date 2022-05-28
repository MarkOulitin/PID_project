import json
import uuid
from numbers import Number
import os
from typing import List

from recommendation_system.recommendation_algorithm import Algorithm
from recommendation_system.types.recommendation_types import SimulationData, PID


class CustomAlgorithmFailed(Exception):
    pass


class CustomAlgorithm(Algorithm):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name

    def recommend(self, samples: List[SimulationData], set_point: Number):
        task_id = uuid.uuid4().__str__()
        param = {'samples': list(map(lambda sample: sample.to_json(), samples)), 'set_point': set_point}
        param = json.dumps(param)
        python_exec_string = 'python3 {} \'{}\' > {} 2> {}'.format(self.file_name, param, task_id, task_id)
        result = os.system(python_exec_string)
        # if result != 0:
        #     raise CustomAlgorithmFailed('Custom algorithm failed with code {}'.format(result))
        with open(task_id) as file:
            try:
                result = json.load(file)
            except Exception as e:
                raise CustomAlgorithmFailed('Invalid return value from algorithm. \nException: [' + str(
                    e) + ']\nOutput: \n[' + file.read() + ']')
        # try:
            os.remove(task_id)
        except:
            pass
        return PID(result['p'], result['i'], result['d'])


# if __name__ == '__main__':
#     print(CustomAlgorithm('/Users/tomsandalon/Desktop/something.py').recommend([
#         SimulationData(1, 2, 3, 4),
#         SimulationData(5, 6, 7, 8)
#     ], 1).p)
