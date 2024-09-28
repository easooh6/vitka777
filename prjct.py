from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)
database = Database('main.db')

# specific item by id
@app.route('/items/<int:item_id>', methods = ['GET'])
def get_book(item_id):
    return database.get_item(item_id)
# create a item
@app.route('/items', methods=['POST'])
def create_item():
    database.add_item(request.json['name'], request.json['price'], description = request.json['description'] if request.json.get('description', None) else '')
    return {'status': 'success'}

# update a item
@app.route('/items/name', methods = ['PUT'])
def update_item_name():
    database.update_item_name(request.json['id'], request.json['name'])
    return {'status': 'success'}

@app.route('/items/price', methods = ['PUT'])
def update_item_price():
    database.update_item_price(request.json['id'], request.json['price'])
    return {'status': 'success'}

@app.route('/items/description', methods = ['PUT'])
def update_item_description():
    database.update_item_description(request.json['id'], request.json['description'])
    return {'status': 'success'}

# Delete a item
@app.route('/items', methods = ['DELETE'])
def delete_item():
    database.delete_item(id = request.json['id'])
    return {'status': 'success'}

# run the flask app
if __name__ == "__main__":
    app.run(debug = True)
    database.close()