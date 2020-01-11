from flask import redirect, render_template, Blueprint, request, flash, current_app, url_for, flash,jsonify
import os
import json

from project.extensions import  csrf

from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017')

db = client.Api

bcz_topic = db['bcz_topic']

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
    return jsonify(data)

@api.route('/classroom/delete')
@csrf.exempt
def delete():
    bcz_topic.drop()
    return 'successfully'

# {'topic':'延伸学习',
#   'h1':'一串单词',
#   'h2': '用记住一个单词的时间,记住一串单词',
#   'articles':{
#       'type1': [
#          '词根，能帮我更快地记单词码？',
#          '你最熟悉的Visa, 它的词根你却不一定熟悉',
#          '一个单纯的词根，带你拧清单词背后的规律',
#          '这个常考的词根，将刷新你对单词的认识',
#          '背过不等于认识，这几个单词教会我的事',
#          '光棍节特辑： 一把带感的狗粮'
#       ],
#       'type2': [
#          '聊聊英语中那些常错的易混词',
#          '成组的单词，我要打包把你们记住',
#          'anti-前缀的单词，你知道多少？',
#          '以-itude结尾的单词，你记得几个？',
#          '学科特辑（一）：从化学元素开始，聊聊词缀-um',
#          '学科特辑（二）：数理化里的单词缩写，你知道吗？',
#          '学科特辑（三）： 太阳系八大行星与罗马希腊神话',
#          '生活特辑（一）：你吃喝玩乐时，也能记住单词',
#          '生活特辑（二）：日常生活设施和物品，你知道怎么说吗？',
#          '生活特辑（三）： 我们吃到的蔬菜水果们',
#          '旅游特辑（一）：出国申请签证会遇到的单词，短语',
#          '旅游特辑（二）：机场里用到的单词',
#          '旅游特辑（三）： 住店，打车，吃饭会用到的英语',
#          '旅游特辑（四）：出国逛商场要用到的单词，短语',
#          '旅游特辑（五）：出国买护肤品，会用到哪些单词？'
#
#       ]
#   }
#  }
