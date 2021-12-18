from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from pprint import pprint
import numpy as np
from numpy import poly1d
from datetime import datetime, timedelta
from scipy import interpolate, optimize
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt



app = Flask(__name__)
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"




def datetime_to_millis_since_epoch(dt):
    return dt.timestamp() * 1000


'''
Random output generator
'''
#
def generate_points(f=poly1d([1,0,0,10000]), n=1000):
    times = []
    for i in range(n):
        times += [datetime_to_millis_since_epoch(datetime.now() + timedelta(0, i))]
    times = list(map(lambda time: time - min(times), times))
    values = [(f(t - 10000)) for t in times]
    return times, values
# data = {'output': [45.138885498046896,
#             45.138885498046896,
#             45.138885498046896,
#             45.138885498046896,
#             45.138885498046896],
#  'time': ['2021-12-18T10:58:02.032376Z',
#           '2021-12-18T10:58:02.032376Z',
#           '2021-12-18T10:58:02.032376Z',
#           '2021-12-18T10:58:02.032376Z',
#           '2021-12-18T10:58:03.046381Z']}
time, value = generate_points()

# possible kinds:
possible_interpolation_methods = ['linear', 'nearest', 'nearest-up', 'zero', 'slinear', 'quadratic', 'cubic', 'previous', 'next', 'zero', 'slinear','quadratic', 'cubic']
def interpolate_data(xs, ys, gaussian_filter_sigma=3.,kind=possible_interpolation_methods[0]):
    # ys = gaussian_filter(ys, gaussian_filter_sigma)
    plt.plot(xs, ys)
    plt.show()
    func = interpolate.UnivariateSpline(xs, ys)
    derivated_twice = func.derivative(n=2)
    result = optimize.root(derivated_twice, x0=(1.))
    pass


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
    data = normalize_data(request.get_json())
    pprint(data)

    response = {
        'inflection': [1.2, 66.6], # (x,y)
        'gradient': 30, # the gradient at (x,y)
    }

    return jsonify(response)


if __name__ == '__main__':
    data = {"time": time, "output": value}
    something = normalize_data(data)
    interpolate_data(something["time"], something["output"])
    # pass
    # times, values = generate_points()
    # print(times, values)
    # app.run(debug=False)