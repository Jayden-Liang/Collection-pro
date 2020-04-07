from flask import make_response, redirect, render_template, Blueprint, request, flash, current_app, url_for, flash,jsonify
import os
import json
import time

from project.extensions import  csrf

from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017')

db = client.Api

bcz_topic = db['bcz_topic']

Memory_Card= db['Memory_Card']
readingList =db['readingList']
dailyNote=db['dailyNote']

api= Blueprint('api', __name__, template_folder='templates', url_prefix='/api')


@api.route('/')
@csrf.exempt
def index():
    return 'hi'

@api.route('/lativ/homedata')
@csrf.exempt
def data():
    data=[{
      "url":'',
      "title":'',
      "price":'',
      "comments":'12'
    }]
    return jsonify(data)

@api.route('/classroom/add')
@csrf.exempt
def classroom():
    print('guge')
    with open ('./project/blueprints/api/data/bcz_topic.txt','r') as f:
        data=f.read()
    data=eval(data)
    bcz_topic.insert(data)
    return 'successfully'

@api.route('/classroom/show')
@csrf.exempt
def show():
    with open ('./project/blueprints/api/data/bcz_all.txt','r') as f:
        data=f.read()

    # data= bcz_topic.find({},{'_id':0})
    # a=[]
    # for x in data:
    #     a.append(x)
    r=make_response(jsonify(data))
    r.headers['Access-Control-Allow-Origin']='http://localhost:8080'
    return r

@api.route('/classroom/delete')
@csrf.exempt
def delete():
    bcz_topic.drop()
    return 'successfully'

@api.route('/xiaochengxu/pic')
@csrf.exempt
def xiaochengxu():
    return render_template('xiaochengxu.html')

@api.route('/memoryCard',methods=['POST','GET'])
@csrf.exempt
def mc():
    data=Memory_Card.find({},{"_id":0})
    rt_data=[]
    for item in data:
        rt_data.append(item)
    if request.method =='POST':
        id=len(rt_data)+1
        data = request.get_json()
        data["tested"]=0
        data["correct"]=0
        data['id']=id
        Memory_Card.insert(data)
        return 'inserted'
    return jsonify(rt_data)

@api.route('/memoryCard/delete',methods=['POST'])
@csrf.exempt
def mc_delete():
    # data= request.get_json()
    Memory_Card.drop()
    return 'ok'


@api.route('/readingList',methods=['POST','GET'])
@csrf.exempt
def reading_list():
    data=readingList.find({},{"_id":0})
    rt_data=[]
    for item in data:
        rt_data.append(item)
    if request.method =='POST':
        id=len(rt_data)+1
        data = request.get_json()
        data['id']=id
        readingList.insert(data)
        return 'inserted'
    return jsonify(rt_data)

@api.route('/readingList/delete',methods=['POST'])
@csrf.exempt
def rl_delete():
    # data= request.get_json()
    readingList.drop()
    return 'ok'



@api.route('/dailyNote',methods=['POST','GET'])
@csrf.exempt
def dailyNote():
    data=dailyNote.find({},{"_id":0})
    rt_data=[]
    for item in data:
        rt_data.append(item)
    if request.method =='POST':
        id=len(rt_data)+1
        data = request.get_json()
        data['id']=id
        dailyNote.insert(data)
        return 'inserted'
    return jsonify(rt_data)
