"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from datetime import datetime
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/post/<int:id>', methods=['DELETE'])
def delete_post(id):
    post_delete = Post.query.filter_by(id=id).delete()
    db.session.commit()
    return "todo ok",200

@app.route('/post', methods=['POST','GET'])
def new_post():
    if (request.method == 'POST'):
        body = request.get_json() #Convierto lo que me llega del front a formato json
        create_post = Post(body['text'])
        db.session.add(create_post) #añado nuevo post a la base de datos
        db.session.commit() #guardamos el cambio en la base de datos
        print (create_post.serialize())
        return jsonify(create_post.serialize()), 201 #mandamos aquí este return al cliente en formato json
    else:
        post_list = Post.query.all() #post_lis tiene todos los posts
        new_list=[]
        for post in post_list:
            new_list.append(post.serialize())
        print(new_list)
        return jsonify(new_list), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
