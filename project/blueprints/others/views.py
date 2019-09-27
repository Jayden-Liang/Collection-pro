from flask import redirect, render_template, Blueprint, request, flash, current_app, url_for, flash, jsonify, abort
from pymongo import MongoClient
from project.extensions import  csrf
import json
import random
import time

Burger= Blueprint('Burger', __name__, template_folder='templates', url_prefix='/burger', static_folder='static',static_url_path="blueprints/others/static" )

client = MongoClient('mongodb://mongo:27017')
db = client.Burger
Ingres = db['Ingres']
auth = db['Auth']
pwdstorage= db['Pwdstorage']
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

@Burger.route('file_password', methods=['POST','GET'])
def file():
    return render_template('indexs.html')

@Burger.route('init_pwd')
def pwd_init():
    pwdstorage.drop()
    pwdstorage.insert({'filePassword': "1234", 'history':[],"date":'9.26'})
    return 'initialed'

# @Burger.route('show_pwd')
# def show_pwd():
#     a=[]
#     for x in pwdstorage.find({},{'_id':0}):
#         a.append(x)
#     return jsonify(a)

@Burger.route('set_pwd')
def reset():
    localtime= time.localtime(time.time())
    newdate= str(localtime.tm_mon)+'.'+str(localtime.tm_mday)
    print(localtime.tm_hour )
    try:
        return jsonify({'filePassword': pwdstorage.find({"date": newdate})[0]['filePassword'],'date':newdate, "askedbefore":'yes'})
    except IndexError:
        newpwd = str(random.randint(1,100000000000))
        pwdstorage.insert({'filePassword': newpwd,'date':newdate})
        return jsonify({'filePassword': newpwd,'date':newdate,"askedbefore":'no'})







    # if pwdstorage.find({"date": newdate}):
        # return jsonify({{'filePassword': pwdstorage.find({"date": newdate})[0]['filePassword'],'date':newdate, "askedbefore":'yes'}})
    # else:
    #     # newpwd = str(random.randint(1,100000000000))
    #     # pwdstorage.insert({'filePassword': newpwd,'date':newdate})
    #     # return jsonify({'filePassword': newpwd,'date':newdate,"askedbefore":'no'})
    #
    #
    # return jsonify({'filePassword': newpwd,'date':newdate})
