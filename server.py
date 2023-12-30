import xmltodict
import json
from flask import Flask
import functions  # Import the functions module

app = Flask(__name__)

with open("file.xml", "r") as file:
    data = json.loads(json.dumps(xmltodict.parse(file.read())))
print(data['server']['routes']['path'][0]['@src'])
for i in range(len(data['server']['routes']['path'])):
    route_src = data['server']['routes']['path'][i]['@src']
    function_name = data['server']['routes']['path'][i]['#text'].lower().replace(" ", "_")
    print(route_src)
    # Ensure the function exists in the functions module
    if hasattr(functions, function_name):
        route_function = getattr(functions, function_name)
        app.route(route_src)(route_function)  # Assign the route
    else:
        print(f"Warning: Function '{function_name}' not found in functions.py")

if __name__ == '__main__':
    app.run(host=data['server']['ip'], debug=eval(data['server']['debug']), port=data['server']['port'])
