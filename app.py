""" 
* API application for testing Flask API with a Machine Learning Model 
* Author: Gregorio Alvarez <allgrego14@gmail.com>
* Last Modification Date: 17-09-2021
* Bauen Intelligence Technology (BIT)
"""

# Import dependencies
from flask import Flask, request, jsonify
import pickle
import numpy as np

# Initialize flask app
app = Flask(__name__)

# Countries list for example
countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

def _find_next_id():
# Function to find next id
    return max(country["id"] for country in countries) + 1

"""""""""""""""""""""""""""""""""" Routes """""""""""""""""""""""""""""""""""""""
""" Only the route '/test' uses the machine learning model """

@app.route('/')
# Display a Hello, World! message
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.get("/countries")
# Get countries list (Can use parameter "id" to get only one)
def get_countries():
    # Get query parameter "id" (0 per default)
    id=request.args.get('id', default=0,type=int)
    # if there is no id
    if not id:
        # return all countries
        return jsonify(countries)
    else:
        # response is error message by default
        response = jsonify({'error': 'Invalid id'})
        # Iterate in list of countries
        for country in countries:
            # Evaluate if country ID is the same as given ID
            if int(id) == int(country['id']):
                print(country)
                response = jsonify(country)
                break
        return response    


""" @app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415 """

""" THIS IS THE ML MODEL ROUTE """
@app.get("/test")
# Get price of a house according to some parameters
# This function gets the result from the ML Model
def test_model():
    # model file name
    filename = 'anibal_model.sav'    
    # load the model from file
    loaded_model = pickle.load(open(filename, 'rb'))
    
    # Get query params (there are default values for each one)
        #['rooms', 'bathroom', 'landsize', 'buildingArea', 'yearBuilt', 'lattitude', 'longtitude']
    rooms=request.args.get('rooms', default=1,type=int)
    bathroom=request.args.get('bathroom', default=2.0,type=float)
    landsize=request.args.get('landsize', default=96.0,type=float)
    buildingArea=request.args.get('buildingArea', default=71.0,type=float)
    yearBuilt=request.args.get('yearBuilt', default=1881,type=int)
    lattitude=request.args.get('lattitude', default=-37.85010,type=float)
    longitude=request.args.get('longitude', default=144.99530,type=float)

    # Array for inputs
    X_test = [[ rooms, bathroom, landsize, buildingArea, yearBuilt, lattitude, longitude]]

    # Array result of prediction with given inputs
    result = loaded_model.predict(X_test)
    # Get first element of prediction array (price of house in USD)
    # And cast it as scalar
    prediction = np.asscalar(result[0])
    # Return response in json
    return jsonify({
        "data":{
            "Rooms": rooms,
            "Bathroom": bathroom,
            "Landsize": landsize,
            "BuildingArea": buildingArea,
            "YearBuilt": yearBuilt,
            "Lattitude": lattitude,
            "Longitude": longitude,
          },
        "result": {
            "currency": "USD",
            "amount": prediction
        }
    }), 200