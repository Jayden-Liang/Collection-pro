from flask import redirect, render_template, Blueprint, request, flash, current_app, url_for, flash, jsonify, abort
from pymongo import MongoClient
from project.extensions import  csrf
import json

Burger= Blueprint('Burger', __name__, template_folder='templates', url_prefix='/burger' )

client = MongoClient('mongodb://mongo:27017')
db = client.Burger
Ingres = db['Ingres']
auth = db['Auth']
# Ingres.insert({
#     "meat":0,
#     "cheese":0,
#     "salad":0
#
# })
@Burger.route('/', methods=['POST','GET'])
@csrf.exempt
def index():
    if request.method=="POST":
        data= request.get_json()
        Ingres.insert(data)
        return jsonify("successfully")
    a=[]
    for x in Ingres.find({},{'_id':0}):
        a.append(x)
    return jsonify(a)

@Burger.route('/auth', methods=['POST','GET'])
@csrf.exempt
def auth():
    if request.method=='POST':
        data= request.get_json()
        print(data)
        rt={
           "status code": "200",
           "status": "successfully"
        }
        if data:
            pass
        # abort(500, message="Fatal error: Pizza the Hutt was found dead earlier")
        return jsonify(rt, 406)

@Burger.route('file_password')
def file():
    return 'hello world'
