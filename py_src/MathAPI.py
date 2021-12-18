from flask import Flask
from flask import jsonify
from flask import request
import sys
from flask import abort
from pprint import pprint
import numpy as np
from numpy import poly1d
from datetime import datetime, timedelta
from scipy import interpolate, optimize
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

app = Flask(__name__)

SLOPE_NEAR_ZERO = "Slope approaches zero"
TIME_ARGUMENT_MISSING = "time argument not provided"
OUTPUT_ARGUMENT_MISSING = "output argument not provided"
BAD_SIZE_OF_ARGUMENTS = "Lengths of parameter arrays is different"
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


'''
Random output generator
'''
#
# def generate_points(f=poly1d([1,0,0,100]), n=1000):
#     times = []
#     for i in range(n):
#         times += [(datetime.now() + timedelta(0, i)).timestamp()]
#     times = list(map(lambda time: time - min(times), times))
#     values = [(f(t - 400)) for t in times]
#     return times, values
# # data = {'output': [45.138885498046896,
# #             45.138885498046896,
# #             45.138885498046896,
# #             45.138885498046896,
# #             45.138885498046896],
# #  'time': ['2021-12-18T10:58:02.032376Z',
# #           '2021-12-18T10:58:02.032376Z',
# #           '2021-12-18T10:58:02.032376Z',
# #           '2021-12-18T10:58:02.032376Z',
# #           '2021-12-18T10:58:03.046381Z']}
# time, value = generate_points()

#TODO make it safer for data
def interpolate_data(xs, ys, slope_thresh = 10**(-3)):
    plt.plot(xs, ys)
    plt.show()
    func = interpolate.UnivariateSpline(xs, ys)
    derivate_once = func.derivative(n=1)
    derivated_twice = derivate_once.derivative(n=1)
    x_root_of_second_derivative = optimize.root(derivated_twice, x0=np.array([[1.]]))['x'][0]
    point = (x_root_of_second_derivative, func(x_root_of_second_derivative).item())
    slope = derivate_once(x_root_of_second_derivative).item()
    if abs(slope) < slope_thresh:
        return None, None, SLOPE_NEAR_ZERO
    return point, slope, None


def time_to_millis(data):
    new_data = {}
    new_data["output"] = data["output"]
    datetime_list = list(map(lambda value: datetime.strptime(value.replace("Z", ""), DATE_TIME_FORMAT), data["time"]))
    time_epoch_list = list(map(lambda time: datetime_to_millis_since_epoch(time), datetime_list))
    new_data["time"] = time_epoch_list
    return new_data


def normalize_data(data):
    new_data = {}
    new_data["output"] = data["output"]
    new_data["time"] = list(map(lambda time: time - min(data["time"]), data["time"]))
    return new_data


@app.route('/', methods=['POST'])
def find_inflection_point_with_gradient():
    # data is json object with 2 attributes:
    # time: timestamps array 
    # output: measurements array
    # arrays are the same size
    # throw exception if not same size or problem with the format
    data = request.get_json()
    check_data_validity(data)
    normalized_data = normalize_data(time_to_millis(data))
    point, slope, err_message = interpolate_data(normalized_data["time"], normalized_data["output"])
    if err_message:
        abort(500, err_message)
    response = {
        'inflection': point, # (x,y)
        'gradient': slope, # the gradient at (x,y)
    }

    return jsonify(response)


def check_data_validity(data):
    if "time" not in data:
        abort(400, TIME_ARGUMENT_MISSING)
    if "output" not in data:
        abort(400, OUTPUT_ARGUMENT_MISSING)
    if len(data["time"]) != len(data["output"]):
        abort(400, BAD_SIZE_OF_ARGUMENTS)


if __name__ == '__main__':
    port = 5000 if len(sys.argv) <= 1 or not sys.argv[1].isnumeric() else int(sys.argv[1])
    app.run(debug=False, port=port)
