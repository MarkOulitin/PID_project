from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from pprint import pprint

app = Flask(__name__)


@app.route('/', methods=['POST'])
def find_inflection_point_with_gradient():
    # data is json object with 2 attributes:
    # time: timestamps array 
    # output: measurements array
    # arrays are the same size
    # throw exception if not same size or problem with the format
    data = request.get_json()
    pprint(data)

    response = {
        'inflection': [1.2, 66.6], # (x,y)
        'gradient': 30, # the gradient at (x,y)
    }

    return jsonify(response)






if __name__ == '__main__':
    app.run(debug=False)