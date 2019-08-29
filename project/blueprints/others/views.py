from flask import redirect, render_template, Blueprint, request, flash, current_app, url_for, flash, jsonify
from pymongo import MongoClient
from project.extensions import  csrf
import json

Ingre= Blueprint('Ingre', __name__, template_folder='templates', url_prefix='/ingre' )

client = MongoClient('mongodb://mongo:27017')
db = client.Burger
Ingres = db['Ingres']
# Ingres.insert({
#     "meat":0,
#     "cheese":0,
#     "salad":0
#
# })
@Ingre.route('/', methods=['POST','GET'])
@csrf.exempt
def index():
    if request.method=="POST":
        data= request.get_json()
        print(data)
        Ingres.insert(data)
        return jsonify('i get it')
    a={}
    for x in Ingres.find({},{'_id':0}):
        a.update(x)
    return jsonify(a)
